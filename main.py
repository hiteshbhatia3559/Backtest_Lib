import pandas as pd
from trade import ohlc_backtest
from util import write_result

if __name__ == "__main__":
    bid = pd.read_csv("bid_ohlc_1min.csv")
    bid.set_index(["Timestamp"], drop=True, inplace=True)
    bid.dropna(inplace=True)
    ask = pd.read_csv("ask_ohlc_1min.csv")
    ask.set_index(["Timestamp"], drop=True, inplace=True)
    ask.dropna(inplace=True)
    # file_list = get_list_of_files('./', '.log')

    # file_list = ['CRUDEOIL.2019FEB.211960.20190121.log','CRUDEOIL.2019FEB.211960.20190128.log']

    # for file in file_list:
    #     parts = file.split('.')
    #     if int(parts[-2]) < 20190129:
    #         file_list.remove(file)

    # pool = multiprocessing.Pool(2)
    # output = pool.map(get_default_backtest, ["bid_ohlc.csv","ask_ohlc.csv"])
    # NORMAL
    # rsi_windows = [14,21,28]  # 3
    # rsi_oversold_bounds = [35,40,45] # 3
    # rsi_overbought_bounds = [50,55,60]  # 3
    # ema_values = [7,21,28,42]  # 4
    # targets = range(400, 800, 100)  # 4
    # stops = [200,300]  # 2
    # overlaps = [True]  # 1


    rsi_windows = [14]  # 3
    rsi_oversold_bounds = [35] # 3
    rsi_overbought_bounds = [50]  # 3
    ema_values = [7,42]  # 4
    targets = [600]  # 4
    stops = [300]  # 2
    overlaps = [True]  # 1

    # lots = int(input("Enter number of lots per signal\n"))
    # max_lots = int(input("Enter number of maximum lots open at any given time\n"))

    # lots, max_lots = 1, 1
    lots = 1
    max_lots = range(5,20)

    for m_lot in max_lots:
        results = ohlc_backtest(bid, ask, rsi_windows, rsi_oversold_bounds, rsi_overbought_bounds, ema_values, targets,
                                stops,
                                overlaps, lots, m_lot, filename_parent="new-test-1min")

        print(results)

        write_result(results,file="Finalresults-1min - {}.csv".format(m_lot))
