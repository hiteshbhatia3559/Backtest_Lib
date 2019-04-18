import pandas as pd
import talib
import matplotlib.pyplot as plt
from util import resample
import csv
import os
from statistics import mean
import numpy as np
import datetime


def make_long(longs, dataframe, row, lots=10, overlap=False, target=900, stop=300):
    # longs is a set of all longs
    # dataframe is a pandas dataframe of asks, used to market exit positions
    # row has our timestamp, entry price at row[0] and row[1] respectively

    # we need to iterate through the dataframe such that when target or stop == open we must close trade

    # check if there is an existing long trade (trade overlap)
    timestamp_of_entry = row[0]

    if overlap:
        for trade in longs:
            try:
                if timestamp_of_entry < trade["timestamp_of_exit"]:
                    return {"timestamp_of_entry": timestamp_of_entry, "type_of_exit": "Overlap"}
                else:
                    break
            except:
                pass

    # This part of the code will be unreachable if there is a trade overlap
    entry_price = row[1]['close']
    target_price = entry_price + target  # 9 rupees up for crude
    stop_price = entry_price - stop  # 3 rupees down for crude
    timestamp_of_exit = None
    type_of_exit = None
    pnl = None

    # type of exit and PNL calculation
    for item in dataframe.iterrows():
        if item[0] > timestamp_of_entry:
            current_price = item[1]['open']
            if current_price >= target_price:  # If target is hit
                type_of_exit = "Win"
                pnl = (current_price - entry_price) * lots
                timestamp_of_exit = item[0]
                break
            elif current_price <= stop_price:  # If stop is hit
                type_of_exit = "Loss"
                pnl = (current_price - entry_price) * lots
                timestamp_of_exit = item[0]
                break

    return {"timestamp_of_entry": timestamp_of_entry,
            "timestamp_of_exit": timestamp_of_exit,
            "entry_price": entry_price,
            "target_price": target_price,
            "stop_price": stop_price,
            "type_of_exit": type_of_exit,
            "pnl": pnl}


def make_short(shorts, dataframe, row, lots=10, overlap=False, target=900, stop=300):
    # shorts is a set of all shorts
    # dataframe is a pandas dataframe of bids, used to market exit positions
    # row has our timestamp, entry price at row[0] and row[1] respectively

    # we need to iterate through the dataframe such that when target or stop == open we must close trade

    # check if there is an existing long trade (trade overlap)
    timestamp_of_entry = row[0]

    if overlap:
        for trade in shorts:
            try:
                if timestamp_of_entry < trade["timestamp_of_exit"]:
                    return {"timestamp_of_entry": timestamp_of_entry, "type_of_exit": "Overlap"}
                else:
                    break
            except:
                pass

    # This part of the code will be unreachable if there is a trade overlap
    entry_price = row[1]['close']
    target_price = entry_price - target  # 9 rupees down for crude
    stop_price = entry_price + stop  # 3 rupees up for crude
    timestamp_of_exit = None
    type_of_exit = None
    pnl = None

    # type of exit and PNL calculation
    for item in dataframe.iterrows():
        if item[0] > timestamp_of_entry:
            current_price = item[1]['open']
            if current_price <= target_price:  # If target is hit
                type_of_exit = "Win"
                pnl = (current_price - entry_price) * lots * (-1)
                timestamp_of_exit = item[0]
                break
            elif current_price >= stop_price:  # If stop is hit
                type_of_exit = "Loss"
                pnl = (current_price - entry_price) * lots * (-1)
                timestamp_of_exit = item[0]
                break

    return {"timestamp_of_entry": timestamp_of_entry,
            "timestamp_of_exit": timestamp_of_exit,
            "entry_price": entry_price,
            "target_price": target_price,
            "stop_price": stop_price,
            "type_of_exit": type_of_exit,
            "pnl": pnl}


def do_backtest(bid, ask, rsi_windows, rsi_oversold_bounds, rsi_overbought_bounds, ema_values, targets, stops,
                overlaps):
    i = 0
    results = []
    for overlap in overlaps:
        for rsi_window in rsi_windows:
            for rsi_upper in rsi_overbought_bounds:
                for rsi_lower in rsi_oversold_bounds:
                    for slow_ema in ema_values:
                        for fast_ema in ema_values:
                            for target in targets:
                                for stop in stops:
                                    settings = "overlap_{}-rsiwindow_{}-rsiupper_{}-rsilower_{}-slowema_{}-fastema_{}-target_{}-stop_{}".format(
                                        overlap, rsi_window, rsi_upper, rsi_lower, slow_ema, fast_ema, target, stop)
                                    # print(settings)
                                    ask['RSI'] = talib.RSI(ask['close'], timeperiod=rsi_window)
                                    ask['MA_fast'] = talib.EMA(ask['close'], timeperiod=fast_ema)
                                    ask['MA_slow'] = talib.EMA(ask['close'], timeperiod=slow_ema)
                                    lots = 10
                                    longs = []
                                    shorts = []

                                    # STRATEGY
                                    # Return type is a dict with
                                    # if valid : {timestamp of entry, timestamp of exit, entry price, target price, stop price, type of exit, pnl}
                                    # if invalid : {timestamp_of_entry, type_of_exit}
                                    # print(row[1]['RSI']) # RSI VALUES HERE, row[0] is index (timestamp)

                                    for row in ask.iterrows():
                                        if row[1]['MA_fast'] > row[1]['MA_slow']:
                                            if row[1]['RSI'] < rsi_lower:  # Oversold condition
                                                longs.append(
                                                    make_long(longs, bid, row, lots=lots, target=target, stop=stop,
                                                              overlap=overlap))
                                        if row[1]['MA_fast'] < row[1]['MA_slow']:
                                            if row[1]['RSI'] > rsi_upper:  # Overbought condition
                                                shorts.append(
                                                    make_short(shorts, ask, row, lots=lots, target=target, stop=stop,
                                                               overlap=overlap))
                                    num_longs, num_shorts = 0, 0
                                    for item in longs:
                                        if item["type_of_exit"] in ["Win", "Loss"]:
                                            num_longs += 1
                                    for item in shorts:
                                        if item["type_of_exit"] in ["Win", "Loss"]:
                                            num_shorts += 1

                                    if num_shorts == 0:
                                        break
                                    if num_longs == 0:
                                        break
                                    # STRATEGY

                                    # PNL Calc
                                    # PNL for longs

                                    longs_pnl = 0
                                    long_turnover = 0
                                    for item in longs:
                                        try:
                                            longs_pnl += item["pnl"]
                                            long_turnover += item["entry_price"] * lots
                                        except:
                                            pass
                                    long_brokerage = long_turnover / 1000000000 * 838
                                    net_long_pnl = longs_pnl - long_brokerage

                                    # PNL for shorts
                                    shorts_pnl = 0
                                    short_turnover = 0

                                    for item in shorts:
                                        try:
                                            shorts_pnl += item['pnl']
                                            short_turnover += item["entry_price"] * lots
                                        except:
                                            pass

                                    short_brokerage = short_turnover / 1000000000 * 838
                                    net_short_pnl = shorts_pnl - short_brokerage
                                    # print("Net PNL long is: " + str(net_long_pnl) + " and Net PNL short is: " + str(net_short_pnl))

                                    long_win, long_loss, short_win, short_loss = 0, 0, 0, 0
                                    for item in longs:
                                        if item["type_of_exit"] == "Win":
                                            long_win += 1
                                        if item["type_of_exit"] == "Win":
                                            long_loss += 1

                                    for item in shorts:
                                        if item["type_of_exit"] == "Win":
                                            short_win += 1
                                        if item["type_of_exit"] == "Win":
                                            short_loss += 1

                                    profitability_longs = long_win / num_longs
                                    profitability_shorts = short_win / num_shorts
                                    profitability_total = (long_win + short_win) / (num_longs + num_shorts)

                                    pnl = []

                                    for item in longs:
                                        pnl.append(item["pnl"])
                                    for item in shorts:
                                        pnl.append(item["pnl"])

                                    total_time_for_every_trade = []
                                    for item in longs:
                                        total_time_for_every_trade.append(
                                            item["timestamp_of_exit"] - item["timestamp_of_entry"])
                                    for item in shorts:
                                        total_time_for_every_trade.append(
                                            item["timestamp_of_exit"] - item["timestamp_of_entry"])

                                    avg_time = sum(total_time_for_every_trade, datetime.timedelta(0)) / len(
                                        total_time_for_every_trade)

                                    # Logic to return data as a result
                                    if net_long_pnl != 0.0:
                                        if net_short_pnl != 0.0:
                                            results.append({"settings": settings,
                                                            "netlongpnl": net_long_pnl,
                                                            "netshortpnl": net_short_pnl,
                                                            "netpnl": net_short_pnl + net_long_pnl,
                                                            "profitability_longs": profitability_longs,
                                                            "profitability_shorts": profitability_shorts,
                                                            "profitability_total": profitability_total,
                                                            "number_of_trades": num_shorts + num_longs,
                                                            "num_longs":num_longs,
                                                            "num_shorts":num_shorts,
                                                            "max_profit": max(pnl),
                                                            "max_DD": min(pnl),
                                                            "average_pnl": mean(pnl),
                                                            "apnl/max_DD": mean(pnl) / abs(min(pnl)),
                                                            "average_trade_time": avg_time
                                                            })
                                    i += 1
                                    print(str(i) + " : " + str(profitability_total) + " : " + str(
                                        net_short_pnl + net_long_pnl) + " : " + str(
                                        num_longs + num_shorts) + " : " + settings)
    return results
