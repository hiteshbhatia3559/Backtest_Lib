import pandas as pd

col_names = ["Timestamp","Remove","Remove","Remove","Remove","B2","B1","B","A","A1","A2"]
filler = ["Remove"] * (36-len(col_names))
col_names += filler
df = pd.read_csv('1 (1).log',header=None,names=col_names)

df.drop(["Remove"],axis=1,inplace=True)
for x in range(1,51):
    try:
        df.drop(["Remove.{}".format(str(x))],axis=1,inplace=True)
    except:
        pass

df.set_index(["Timestamp"],inplace=True)
df.drop(df.index[50],inplace=True)
df.drop(df.index[-50],inplace=True)

print(df.head(1).index)
