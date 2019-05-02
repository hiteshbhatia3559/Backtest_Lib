import csv
from util import get_list_of_files
import pandas as pd
import matplotlib.pyplot as plt

file_list = get_list_of_files('./', '.csv')

df_array = []

for file in file_list:
    df = pd.read_csv(file).sort_values(by="netpnl", axis=0, ascending=False).head(1)
    df = df.reset_index(drop=True)
    df_array.append(df)

for item in df_array:
    print(str(item["settings"].iloc[0])+" : "+str(item["netpnl"].iloc[0]/100))
