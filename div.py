import os
import pandas as pd
import numpy as np
import itertools

df = pd.read_excel('제조업.xlsx', header=9, dtype={'종목코드':'object'})
df = pd.DataFrame(np.where(df.values == 0, np.nan, df.values), index=df.index, columns=df.columns)
years = np.arange(2019, 2007, -1)

for y_a, y_b in itertools.product(years, years):
    if y_a - y_b == 1:
        y_a = str(y_a)
        y_b = str(y_b)
        df.loc[:, '{0}~{1}'.format(y_a, y_b)] = np.where(df[y_a] >= df[y_b], True, False)
        
cols = []
for y_a, y_b in itertools.product(years, years):
    if y_a - y_b == 1:
        y_a = str(y_a)
        y_b = str(y_b)
        cols.append(y_a + '~' + y_b)
        
for idx in df.index:
    tmp = df.loc[idx]
    i = 0
    for c in cols:
        if tmp.loc[c] == True:
            i += 1
        if tmp.loc[c] == False:
            break
    df.loc[idx, '지속성장년도'] = i
    
df['지속성장년도'].value_counts()
            
