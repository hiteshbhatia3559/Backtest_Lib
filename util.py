import pandas as pd
import talib
import matplotlib.pyplot as plt
import matplotlib.dates as md
from os import listdir
from os.path import isfile, join
import os
import csv

def resample(filename, timeframe='15Min'):
    # Get top bid ask
    col_names = ["Timestamp", "Remove", "Remove", "Remove", "Remove", "B2", "B1", "B", "A", "A1", "A2"]
    filler = ["Remove"] * (36 - len(col_names))
    for item in filler:
        col_names.append(item)
    df = pd.read_csv(filename, header=None, names=col_names)[50:-50]

    # Cleaning
    df.drop(["Remove"], axis=1, inplace=True)
    for x in range(1, 51):
        try:
            df.drop(["Remove.{}".format(str(x))], axis=1, inplace=True)
        except:
            pass

    # Convert epoch to Indian datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'] * 1e9).values + pd.to_timedelta(5.5, unit='h')

    # Set index as Timestamp
    df.set_index(df['Timestamp'], inplace=True)

    # Drop duplicate Timestamp column
    df.drop(['Timestamp'], axis=1, inplace=True)

    # Convert Bid-Ask to int
    df[["B", "A"]] = df[["B", "A"]].astype(int)

    # Get bid ohlc
    bid = df["B"].resample(timeframe).ohlc()

    # Get ask ohlc
    ask = df["A"].resample(timeframe).ohlc()

    # Return bid, ask
    return bid, ask

def write_result(results,file):
    with open("{}.csv".format(file), "w+", newline="") as outfile:
        keys = results[0].keys()
        dict_writer = csv.DictWriter(outfile,keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    return "Done for {}".format(file)

def get_list_of_files(relative_path,extension):
    onlyfiles = [f for f in listdir(relative_path) if isfile(join(relative_path, f))]

    file_list = []

    for filename in onlyfiles:
        if extension in filename:
            file_list.append(filename)

    return file_list

def write_trades(settings,trades):
    # nocare = os.system("mkdir results")
    keys = trades[0].keys()
    with open('./results/{}.csv'.format(settings),'w+',newline='') as outfile:
        dict_writer = csv.DictWriter(outfile,keys)
        dict_writer.writeheader()
        dict_writer.writerows(trades)

    # print("Written file for {}".format(settings))

if __name__ == "__main__":

    x, y = resample('1 (5).log', '1Min')
    x = x/100

    plt.plot(x)
    plt.show()
