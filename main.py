import pandas as pd
import talib
import matplotlib.pyplot as plt
from resample import resample
from trade import make_long, make_short

bid, ask = resample('1 (1).log', '1Min')

rsi_windows = range(5, 50)
rsi_oversold_bounds = range(10, 50)
rsi_overbought_bounds = range(50, 90)
ema_values = range(10, 100)

ask['RSI'] = talib.RSI(ask['close'], timeperiod=28)
ask['MA14'] = talib.EMA(ask['close'], timeperiod=14)
ask['MA28'] = talib.EMA(ask['close'], timeperiod=28)

longs = []
shorts = []
overlap = False
# STRATEGY
# Return type is a dict with
# if valid : {timestamp of entry, timestamp of exit, entry price, target price, stop price, type of exit, pnl}
# if invalid : {timestamp_of_entry, type_of_exit}
# print(row[1]['RSI']) # RSI VALUES HERE, row[0] is index (timestamp)
for row in ask.iterrows():
    if row[1]['MA14'] > row[1]['MA28']:
        if row[1]['RSI'] < 50:  # Oversold condition
            longs.append(make_long(longs, bid, row, lots=10, target=200, stop=200,overlap=overlap))
    if row[1]['MA14'] < row[1]['MA28']:
        if row[1]['RSI'] > 50:
            shorts.append(make_short(shorts, ask, row, lots=10, target=200, stop=200,overlap=overlap))
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
print("Net PNL long is: " + str(net_long_pnl) + " and Net PNL short is: " + str(net_short_pnl))

num_longs, num_shorts = 0, 0
for item in longs:
    if item["type_of_exit"] in ["Win", "Loss"]:
        num_longs += 1
for item in shorts:
    if item["type_of_exit"] in ["Win", "Loss"]:
        num_shorts += 1

print("Longs to Shorts ratio : "+str(num_longs)+":"+str(num_shorts)+" -- For a total of "+str(num_longs+num_shorts))
