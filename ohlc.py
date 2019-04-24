from util import resample,get_list_of_files
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

file_list = get_list_of_files('./','log')

bids = []
asks = []

for file in tqdm(file_list):
    bid, ask = resample(file,'1Min')
    bids.append(bid)
    asks.append(ask)

main = pd.DataFrame(bids[0])
main1 = pd.DataFrame(asks[0])

for bid in bids[1:]:
    main = main.append(bid)

for ask in asks[1:]:
    main1 = main1.append(ask)


main.sort_index(inplace=True)
main1.sort_index(inplace=True)

main.to_csv(r'bid_ohlc_1min.csv')
main1.to_csv(r'ask_ohlc_1min.csv')


# # PART 2
# df = pd.read_csv("bid_ohlc.csv")
# df.set_index(["Timestamp"],drop=True,inplace=True)
#
# print(df)
