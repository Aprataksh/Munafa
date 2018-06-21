import csv
import fnmatch
import os
import sys
import pandas as pd
import collections
import logging
sys.path.insert(0, r"..\utilities")
import config
import get_ticker_list

obj=config.config(r"../config.txt")

def HA(ticker,df):
    df['HA_Close']=(df['Open']+ df['High']+ df['Low']+df['Close'])/4
    idx = df.index.name
    df.reset_index(inplace=True)
    df.at[0, 'HA_Open'] = ((df.at[0, 'Open'] + df.at[0, 'Close']) / 2)
    nt = collections.namedtuple('nt', ['Open','Close'])
    previous_row = nt(df.ix[0,'Open'],df.ix[0,'Close'])
    i=0
    for row in df.itertuples():
        if i==0:
            i+=1
            continue
        ha_open=(previous_row.Open + previous_row.Close) / 2
        df.at[i,'HA_Open']=ha_open
        previous_row = nt(row.Open, row.Close)
        i+=1
    if idx:
        df.set_index(idx, inplace=True)
    df['HA_High']=df[['Open','Close','High']].max(axis=1)
    df['HA_Low']=df[['Open','Close','Low']].min(axis=1)
    df = df.drop(['Open', 'High', 'Low', 'Close'], axis=1)
    df = df.rename(columns={"HA_Open": "Open", "HA_High": "High", "HA_Low": "Low", "HA_Close": "Close", "Volume": "Volume"})
    df = df[['Close', 'High', 'Low', 'Open', 'Volume']]
    df.to_csv(obj.path_to_output_dir()+"Heikin-Ashi/"+ticker+'.csv')

def convert_to_df(ticker,path_to_data):
    rows = []
    times = []
    columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    with open(path_to_data+ticker+".csv",'r') as f:
        lines= csv.reader(f)
        for line in lines:
            if 'Close' in line:
                continue
            times.append(line[0])
            rows.append(map(float,line[1:]))
        df = pd.DataFrame(rows,index=pd.DatetimeIndex(times, name='Date Time'),columns=columns)
        return df
    
def main(path_to_data):
    c=0
    ticker_list=get_ticker_list.get_ticker_list(obj.path_to_master_list())
    for ticker in ticker_list:
        print(ticker)
        df=convert_to_df(ticker,path_to_data)
        HA(ticker,df)
    # To find the number of files in the output directory that end with .csv i.e. are the output files of the tickers
    list=os.listdir(obj.path_to_output_dir()+"Heikin-Ashi/")
    length_1=len(fnmatch.filter(list, "*.csv"))
    #to find the number of tickers in the master list
    ticker_list=get_ticker_list.get_ticker_list(obj.path_to_master_list())

