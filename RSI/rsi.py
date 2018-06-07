import csv
import pandas as pd
from stockstats import StockDataFrame as Sdf
import matplotlib.pyplot as plt

class RSI:
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
            print(rsi_df)
            #rsi_df.to_csv(r"C:\Users\microsoft\Desktop\5mindata/"+self.ticker+"_rsi.csv")
            rsi_df.to_csv(r"C:\Users\Rohit\Python_source_code\output\RSI/" + self.ticker + "_rsi.csv")
            plt.plot(rsi_df['RSI'],color='red')
            plt.show()

def main():
    #obj=RSI(4,"3MINDIA",r"C:\Users\microsoft\Desktop\5mindata\3MINDIA.csv")
    obj=RSI(14,"3MINDIA",r"C:\Users\Rohit\Python_source_code\historical_stock_5_min_data\3MINDIA.csv")
    obj.calculate_rsi()
main()
