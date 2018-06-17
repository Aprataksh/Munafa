import csv
import sys
import pandas as pd
from stockstats import StockDataFrame as Sdf
import matplotlib.pyplot as plt
sys.path.insert(0, r"..\utilities")
import config
import get_ticker_list

class RSI:
    obj = config.config(r"../config.txt")

    def __init__(self,p,ticker,path):
        self.period=p
        self.ticker=ticker
        self.path_to_ticker_data=path

    def calculate_rsi(self):
        rows = []
        times = []
        columns = ['Close', 'High', 'Low', 'Open', 'Volume']
        with open(self.path_to_ticker_data,'r') as f:
            lines = csv.reader(f)
            for line in lines:
                if 'Close' not in line:
                    times.append(line[0])
                    rows.append(map(float,line[1:]))
            df = pd.DataFrame(rows,index=pd.DatetimeIndex(times, name='Date Time'),columns=columns)
            stock_df = Sdf.retype(df)
            rsi_text="rsi_"+str(self.period)
            df['rsi'] = stock_df[rsi_text]
            rsi=list(df['rsi'])
            rsi_df=pd.DataFrame(rsi,index=pd.DatetimeIndex(times, name='Date Time'),columns=['RSI'])
            #print(rsi_df)
            rsi_df.to_csv(self.obj.path_to_output_dir()+"RSI/" + self.ticker + "_rsi.csv")
            #plt.plot(rsi_df['RSI'],color='red')
            #plt.show()

def main():
    period=14
    obj = config.config(r"../config.txt")
    ticker_list=get_ticker_list.get_ticker_list(obj.path_to_master_list())
    for ticker in ticker_list:
        print(ticker)
        rsi_obj=RSI(period,ticker,obj.path_to_historical_5_min_dir()+ticker+".csv")
        rsi_obj.calculate_rsi()
main()
