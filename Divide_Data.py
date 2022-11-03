import pandas as pd

df = pd.read_table('cme.20210709.c.pa2')
df['lenth'] = df.apply(lambda row:len(row[0]),axis=1)
# print(df.groupby('lenth').head(1))
groups = df.groupby(df.lenth)
df_B = groups.get_group(183)
df_eight = groups.get_group(126)
print('Group type B:')
print(df_B)
print('Group type 81 82:')
print(df_eight)
df = pd.concat([df_B,df_eight])
df.to_csv('CL_expirations_and_settlements.txt',sep='\t',index=False)
