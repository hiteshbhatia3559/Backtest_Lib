from util import resample, write_result, get_list_of_files
from trade import do_backtest

if __name__ == "__main__":

    mypath = "./"

    file_list = get_list_of_files('./', '.log')

    file_list = ['1 (2).log']

    for file in file_list:
        bid, ask = resample(file, '5Min')
        rsi_windows = range(7, 36, 7)  # 5
        rsi_oversold_bounds = range(15, 50, 5)  # 7
        rsi_overbought_bounds = range(50, 85, 5)  # 7
        ema_values = range(7, 70, 7)  # 10
        targets = range(800, 20000, 200)  # 25
        stops = [800, 1000]  # 2
        overlaps = [False,True]  # 0

        results = do_backtest(bid, ask, rsi_windows, rsi_oversold_bounds, rsi_overbought_bounds, ema_values, targets,
                              stops,
                              overlaps)

        status = write_result(results, file)

