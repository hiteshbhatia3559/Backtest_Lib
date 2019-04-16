import pandas as pd
import talib
import matplotlib.pyplot as plt
from resample import resample
from trade import make_long, make_short

bid, ask = resample('1 (1).log', '1s')

ask['RSI'] = talib.RSI(ask['close'], timeperiod=28)
ask['MA14'] = talib.EMA(ask['close'], timeperiod=14)
ask['MA28'] = talib.EMA(ask['close'], timeperiod=28)

longs = []
shorts = []

for row in ask.iterrows():
    # print(row[1]['RSI']) # RSI VALUES HERE, row[0] is index (timestamp)
    if row[1]['RSI'] < 40:  # Oversold condition
        longs.append(make_long(longs, bid, row, lots=1))
        # Return type is a dict with
        # if valid : {timestamp of entry, timestamp of exit, entry price, target price, stop price, type of exit, pnl}
        # if invalid : None
    if row[1]['RSI'] > 60:
        shorts.append(make_short(shorts,ask,row,lots=10))

longs_pnl = 0
for item in longs:
    try:
        longs_pnl += item['pnl']
    except:
        pass
print(longs_pnl)
