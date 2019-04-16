import pandas as pd
import talib
import matplotlib.pyplot as plt
import matplotlib.dates as md

def resample(filename, timeframe='15Min'):
    col_names = ["Timestamp", "Remove", "Remove", "Remove", "Remove", "B2", "B1", "B", "A", "A1", "A2"]
    filler = ["Remove"] * (36 - len(col_names))
    col_names += filler
    df = pd.read_csv(filename, header=None, names=col_names)

    df.drop(["Remove"], axis=1, inplace=True)
    for x in range(1, 51):
        try:
            df.drop(["Remove.{}".format(str(x))], axis=1, inplace=True)
        except:
            pass

    df['Timestamp'] = pd.to_datetime(df['Timestamp']*1e9).values + pd.to_timedelta(5.5, unit='h')
    #print(df['Timestamp'])
    df.set_index(["Timestamp"], inplace=True)
    df[["B", "A"]] = df[["B", "A"]].astype(int)
    df = df.resample(timeframe).ohlc()

    return df["B"], df["A"] # Returns bid and ask OHLC


if __name__ == "__main__":

    x, y = resample('1 (1).log', '1s')
    x.to_csv('new.csv')
    x['RSI'] = talib.RSI(x['open'], timeperiod=36)
    x['MA14'] = talib.EMA(x['close'], timeperiod=36)
    x['MA28'] = talib.EMA(x['close'], timeperiod=72)
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)

    ax1.plot(x['close'])
    print(x['open'].std())
    print(x['open'].mean())
    print(x['open'].head())

    ax2.plot(x['RSI'])
    plt.show()
