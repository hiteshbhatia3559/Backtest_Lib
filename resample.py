import pandas as pd
import talib
import matplotlib.pyplot as plt


def resample(filename, timeframe='15min'):
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
    #print(df['Timestamp'])
    #df.drop(df.index[50], inplace=True)
    #df.drop(df.index[-50], inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp']*1e9).values + pd.to_timedelta(5.5, unit='h')
    #print(df['Timestamp'])
    df.set_index(["Timestamp"], inplace=True)

    #df.index = pd.to_datetime(df.index, unit='m')

    df[["B", "A"]] = df[["B", "A"]].astype(int)
    df = df.resample(timeframe).ohlc()

    #print(df)
    return df["B"], df["A"]


if __name__ == "__main__":
    x, y = resample('1 (1).log', '15Min')



    x.to_csv('new.csv')

    x['RSI'] = talib.RSI(x['open'], timeperiod=36)
    x['MA14'] = talib.EMA(x['close'], timeperiod=36)
    x['MA28'] = talib.EMA(x['close'], timeperiod=72)
    # f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    #plt.plot(x['high'].tail(600))
    #plt.plot(x['low'].tail(600))
    print(x['open'].std())
    print(x['open'].mean())
    print(x['open'].head())



    # ax1.plot(y['close'])
    # ax1.plot(x['MA14'])
    # ax1.plot(x['MA28'])
    # ax2.plot(x['RSI'])
    plt.show()
