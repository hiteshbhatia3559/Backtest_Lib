import pandas as pd

col_names = ["Timestamp", "Remove", "Remove", "Remove", "Remove", "B2", "B1", "B", "A", "A1", "A2"]
filler = ["Remove"] * (36 - len(col_names))
col_names += filler
df = pd.read_csv('1 (1).log', header=None, names=col_names)

df.drop(["Remove"], axis=1, inplace=True)
for x in range(1, 29):
    df.drop(["Remove.{}".format(str(x))], axis=1, inplace=True)

df['Timestamp'] = pd.to_datetime(df['Timestamp'] * 1e9).values + pd.to_timedelta(5.5, unit='h')
# print(df['Timestamp'])
df.set_index(["Timestamp"], inplace=True)
df[["B", "A"]] = df[["B", "A"]].astype(int)
df = df.resample('5Min').ohlc()

print(df)
