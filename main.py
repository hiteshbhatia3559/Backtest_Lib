from util import get_list_of_files
from trade import get_default_backtest
import multiprocessing

if __name__ == "__main__":

    file_list = get_list_of_files('./', '.log')

    # file_list = ['CRUDEOIL.2019FEB.211960.20190121.log','CRUDEOIL.2019FEB.211960.20190128.log']

    # for file in file_list:
    #     parts = file.split('.')
    #     if int(parts[-2]) < 20190129:
    #         file_list.remove(file)

    pool = multiprocessing.Pool(2)
    output = pool.map(get_default_backtest, file_list)

    print(output)
