# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 22:22:46 2020

@author: right
"""

import os
import pandas as pd
import numpy as np

os.chdir(r'C:\Users\right\Documents\CCR')

last_bsns_year = 2019

years = [last_bsns_year - i for i in range(6)]
years = list(map(str, years))

dfs = []
cols = ['자산', '재고자산', '매출채권', '현금', '무형자산', '부채', '매입채무',
        '자본', '매출액', '매출원가', '당기순이익', '영업현금흐름',
        '투자현금흐름', '배당금']

for y in years:
    df = pd.read_excel('연간_{}.xlsx'.format(y), header=10, dtype={'종목코드': 'object'})
    df.set_index('종목코드', inplace=True)
    
    if y == str(last_bsns_year):
        dfs.append(df[['종목명', '업종명', '단위']])
        
    df.drop(['종목명', '업종명', '단위'], axis=1, inplace=True)
    df.columns = list(map(lambda x: x + '_{}'.format(y), cols))
    dfs.append(df)

result = dfs[0].merge(dfs[1], how='left', left_index=True, right_index=True)
result = result.merge(dfs[2], how='left', left_index=True, right_index=True)
result = result.merge(dfs[3], how='left', left_index=True, right_index=True)
result = result.merge(dfs[4], how='left', left_index=True, right_index=True)
result = result.merge(dfs[5], how='left', left_index=True, right_index=True)
result = result.merge(dfs[6], how='left', left_index=True, right_index=True)

result['CCR_2019'] = result['영업현금흐름_2019'] / result['당기순이익_2019']
result['CCR_2018'] = result['영업현금흐름_2018'] / result['당기순이익_2018']
result['CCR_2017'] = result['영업현금흐름_2017'] / result['당기순이익_2017'] 
result['CCR_2016'] = result['영업현금흐름_2016'] / result['당기순이익_2016']
result['CCR_2015'] = result['영업현금흐름_2015'] / result['당기순이익_2015']

result['현금자산비율'] = result['현금_2019'] / result['자산_2019']

result['무형자산총자산비율'] = result['무형자산_2019'] / result['자산_2019']

result['부채비율'] = result['부채_2019'] / result['자본_2019']

result['재고자산회전일수'] = (result['재고자산_2018'] + result['재고자산_2019']) / 2 / result['매출액_2019']
result['매출채권회전일수'] = (result['매출채권_2018'] + result['매출채권_2019']) / 2 / result['매출액_2019']
result['매입채무회전일수'] = (result['매입채무_2018'] + result['매입채무_2019']) / 2 / result['매출액_2019']

result['CCC'] = result['재고자산회전일수'] + result['매출채권회전일수'] - result['매입채무회전일수']
result['당기순이익률'] = result['당기순이익_2019'] / result['매출액_2019']
result['적정보유현금'] = result['매출액_2019'] * (1 - result['당기순이익률']) * (result['CCC'] / 365)
result['현금보유율'] = result['현금_2019'] / result['적정보유현금']
result.to_excel('2020년 종목선정 필터링.xlsx')

result['잉여현금흐름_2019'] = result['영업현금흐름_2019'] + result['투자현금흐름_2019']
result['잉여현금흐름_2018'] = result['영업현금흐름_2018'] + result['투자현금흐름_2018']
result['잉여현금흐름_2017'] = result['영업현금흐름_2017'] + result['투자현금흐름_2017']
result['잉여현금흐름_2016'] = result['영업현금흐름_2016'] + result['투자현금흐름_2016']
result['잉여현금흐름_2015'] = result['영업현금흐름_2015'] + result['투자현금흐름_2015']
result['잉여현금흐름평균'] = (result['잉여현금흐름_2019'] + result['잉여현금흐름_2018'] + result['잉여현금흐름_2017'] + result['잉여현금흐름_2016'] + result['잉여현금흐름_2015']) / 5
result['잉여현금흐름가중평균'] = 5/15*result['잉여현금흐름_2019'] + 4/15*result['잉여현금흐름_2018'] + 3/15*result['잉여현금흐름_2017'] + 2/15*result['잉여현금흐름_2016'] + 1/15*result['잉여현금흐름_2015']

result['시가총액'] = np.nan
result['PFCF'] = np.nan

# 필터링
result = result.loc[
        (result['CCR_2019'] >= 1) &
        (result['CCR_2018'] >= 1) &
        (result['CCR_2017'] >= 1) &
        (result['CCR_2016'] >= 1) &
        (result['CCR_2015'] >= 1) &
        (result['현금자산비율'] >= 0.1) &
        (result['무형자산총자산비율'] < 0.15) &
        (result['부채비율'] < 0.5) &
        (result['현금보유율'] > 1) &
        (~pd.isna(result['배당금_2019'])) &
        (result['잉여현금흐름평균'] > 0)
]

