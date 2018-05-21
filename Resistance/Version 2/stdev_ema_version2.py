import csv
import pandas as pd
import statistics
import math

def get_ticker_list():
    with open(r"C:\Users\Rohit\Python_source_code\nse 500 stock data\nifty500_list.csv", 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                ticker_list.append(line[2])
        print(ticker_list)

ticker_list = []
def main():
    stdev_list = []
    get_ticker_list()
    for ticker in ticker_list:
        if '&' in ticker:
            ticker = ticker[:ticker.index('&')] + "%26" + ticker[ticker.index('&') + 1:]
        print(ticker)
        df = pd.read_csv(r"C:/Users/Rohit/Python_source_code/nse 500 stock data/" + ticker + ".csv")
        ndays = 9
        if len(df.columns) >= 6 and len(df.index) >= ndays:
            SMA = pd.Series(round((df['Close']).rolling(window=ndays).mean(), 2), name='SMA')
            df = df.join(SMA)
            SMA_list = (df['SMA']).tolist()
            SD = round(statistics.stdev(SMA_list[ndays-1:]), 2)
            AV = round(statistics.mean(SMA_list[ndays-1:]), 2)
            volatility = round(SD/AV *100, 2)
            stdev_list.append(volatility)
            EMA = pd.Series(round((df['Close']).ewm(min_periods=ndays, span=15).mean(), 2), name="EMA")
            df = df.join(EMA)
            """df.to_csv(r"C:/Users/Hp/Desktop/New folder/Top500_stock/With SMA and EMA/" + ticker + ".csv")"""
        else:
            stdev_list.append(0)

    sdf = pd.DataFrame(stdev_list, index=pd.Series(ticker_list, name="Ticker"), columns=["Standard Deviation"])
    sdf.to_csv(r"C:\Users\Rohit\Python_source_code\volatility\st_dev.csv")

main()
