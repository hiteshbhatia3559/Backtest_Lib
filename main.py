from util import get_list_of_files
from trade import get_default_backtest
import multiprocessing

if __name__ == "__main__":

    file_list = get_list_of_files('./', '.log')

    pool = multiprocessing.Pool(2)
    output = pool.map(get_default_backtest, file_list)

    print(output)
