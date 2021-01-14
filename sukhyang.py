import os
import pandas as pd

PATH = 
FILENAME = 
DIVIDEND_RATE = 1.02

class SUKHYANG:

    def __init__(self, PATH, FILENAME, DIVIDEND_RATE):
    
        self._path = PATH
        self._filename = FILENAME
        self._dividend_rate = DIVIDEND_RATE
        
        self._get_data()
        self._condition()
        
    def _get_data(self):
        self.df = pd.read_csv(os.path.join(self._path, self._filename), engine='python')
        
    def _condition(self):
    
        condition1 = self.df['발표 PER'] <= 10
        condition2 = self.df['발표 PBR'] <= 1
        condition3 = self.df['시가 배당률 (%)'] >= self._dividend_rate
        condition4 = self.df['당좌 비율 (%)'] >= 100
        
        self.df = self.df.loc[condition1 & condition2 & condition3 & condition4]
        self.df = self.df.loc[self.df['본사 국내 =1'] == 1]
        self.df = self.df.loc[self.df['지주사 =1'] != 1]
        self.df = self.df.loc[self.df['스팩 =1'] != 1]
        self.df = self.df.loc[self.df['관리 종목 =1'] !=1]
        
    def extract_cols(self):
    
        cols = ['코드 번호', '회사명', '자본 (억)', '상장주식수 (만주)', '19년 순이익', '18년 순이익', '17년 순이익']
        return self.df[cols]
        
'''
내재가치 = (BPS + EPS * 10) / 2

EPS = {(최근 연도 EPS * 3) + (전년도 EPS * 2) + (전전년도 EPS * 1)} / 6
BPS = 자기자본 / 주식수
EPS = 당기순이익 / 주식수
'''

sukhyang = SUKHYANG(PATH, FILENAME, DIVIDEND_RATE)
df = sukhyang.extract_cols()

df.loc[:, 'BPS'] = (df.loc[:, '자본 (억)'] * 100000000) / (df.loc[:, '상품주식수 (만주)'] * 10000)
df.loc[:, '최근연도EPS'] = (df.loc[:, '19년 순이익'] * 100000000) / (df.loc[:, '상품주식수 (만주)'] * 10000)
df.loc[:, '전년도EPS'] = (df.loc[:, '18년 순이익'] * 100000000) / (df.loc[:, '상품주식수 (만주)'] * 10000)
df.loc[:, '전전년도EPS'] = (df.loc[:, '17년 순이익'] * 100000000) / (df.loc[:, '상품주식수 (만주)'] * 10000)
df.loc[:, 'EPS'] = ((df.loc[:, '최근연도EPS'] * 3) + (df.loc[:, '전년도EPS'] * 2) + (df.loc[:, '전전년도EPS'] * 1)) / 6
df.loc[:, '적정가'] = (df.loc[:, 'BPS'] + df.loc[:, 'EPS'] * 10) / 2



