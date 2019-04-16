import pandas as pd
import talib
import matplotlib.pyplot as plt
from resample import resample
from trade import make_long, make_short
import csv

bid, ask = resample('1 (1).log', '1Min')

rsi_windows = range(5, 50)
rsi_oversold_bounds = range(10, 50)
rsi_overbought_bounds = range(50, 90)
ema_values = range(10, 100)
targets = range(100,2000,100)
stops = range(100,2000,100)
overlaps = [True,False]

results = []
for overlap in overlaps:
    for rsi_window in rsi_windows:
        for rsi_upper in rsi_overbought_bounds:
            for rsi_lower in rsi_oversold_bounds:
                for slow_ema in ema_values:
                    for fast_ema in ema_values:
                        for target in targets:
                            for stop in stops:
                                settings = "overlap_{}-rsiwindow_{}-rsiupper_{}-rsilower_{}-slowema_{}-fastema_{}-target_{}-stop_{}".format(overlap,rsi_window,rsi_upper,rsi_lower,slow_ema,fast_ema,target,stop)
                                ask['RSI'] = talib.RSI(ask['close'], timeperiod=rsi_window)
                                ask['MA_fast'] = talib.EMA(ask['close'], timeperiod=fast_ema)
                                ask['MA_slow'] = talib.EMA(ask['close'], timeperiod=slow_ema)

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
                                            longs.append(make_long(longs, bid, row, lots=10, target=target, stop=stop, overlap=overlap))
                                    if row[1]['MA_fast'] < row[1]['MA_slow']:
                                        if row[1]['RSI'] > rsi_upper: # Overbought condition
                                            shorts.append(make_short(shorts, ask, row, lots=10, target=stop, stop=stop, overlap=overlap))
                                # STRATEGY

                                # PNL Calc
                                # PNL for longs

                                longs_pnl = 0
                                long_turnover = 0
                                for item in longs:
                                    try:
                                        longs_pnl += item["pnl"]
                                        long_turnover += item["entry_price"] * 10
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
                                        short_turnover += item["entry_price"] * 10
                                    except:
                                        pass

                                short_brokerage = short_turnover / 1000000000 * 838
                                net_short_pnl = shorts_pnl - short_brokerage
                                # print("Net PNL long is: " + str(net_long_pnl) + " and Net PNL short is: " + str(net_short_pnl))

                                num_longs, num_shorts = 0, 0
                                for item in longs:
                                    if item["type_of_exit"] in ["Win", "Loss"]:
                                        num_longs += 1
                                for item in shorts:
                                    if item["type_of_exit"] in ["Win", "Loss"]:
                                        num_shorts += 1

                                # print("Longs to Shorts ratio : " + str(num_longs) + ":" + str(num_shorts) + " -- For a total of " + str(
                                    num_longs + num_shorts

                                with open('output_{}.csv'.format(settings), 'w+') as output:
                                    writer = csv.writer(output)  # writer.writerow to write rows
                                    new = list(longs[0].keys())
                                    writer.writerow(new)
                                    for each in longs:
                                        if each["type_of_exit"] in ["Win", "Loss"]:
                                            # print(each)
                                            writer.writerow(list(each.values()))
                                    for each in shorts:
                                        if each["type_of_exit"] in ["Win", "Loss"]:
                                            # print(each)
                                            writer.writerow(list(each.values()))
                                    print(settings+"Sent to csv")

