import pandas as pd
import talib
import matplotlib.pyplot as plt
from resample import resample
from trade import make_long, make_short
import csv
import os
from statistics import mean
import numpy as np
import datetime
bid, ask = resample('1 (1).log', '5Min')

rsi_windows = range(14, 15)  # 45
rsi_oversold_bounds = range(28, 31)  # 40
rsi_overbought_bounds = range(68, 75)  # 40
ema_values = [14,28]
targets = [200,300,400,500,600,700,800]
stops = [200,300]  # 19
overlaps = [False]  # 2
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

                                profitability_longs = 0
                                profitability_shorts = 0
                                profitability_total = 0

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
                                    total_time_for_every_trade.append(item["timestamp_of_exit"]-item["timestamp_of_entry"])
                                for item in shorts:
                                    total_time_for_every_trade.append(item["timestamp_of_exit"]-item["timestamp_of_entry"])

                                avg_time = sum(total_time_for_every_trade, datetime.timedelta(0)) / len(total_time_for_every_trade)



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
                                                        "number_of_trades":num_shorts+num_longs,
                                                        "max_profit":max(pnl),
                                                        "max_DD":min(pnl),
                                                        "average_pnl":mean(pnl),
                                                        "apnl/max_DD":mean(pnl)/abs(min(pnl)),
                                                        "average_trade_time":avg_time

                                                        })
                                i += 1
                                print(str(i) + " : " + str(profitability_total)+" : "+str(net_short_pnl + net_long_pnl)+" : "+str(num_longs+num_shorts)+" : "+settings)

with open("Results.csv","w+", newline="") as outfile:
    for header in list(results[0].keys()):
        if header != list(results[0].keys())[-1]:
            outfile.write(str(header)+",")
        else:
            outfile.write(str(header)+"\n")
    for result in results:
        for value in list(result.values()):
            if value != list(result.values())[-1]:
                outfile.write(str(value) + ",")
            else:
                outfile.write(str(value) + "\n")

