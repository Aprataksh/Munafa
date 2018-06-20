import csv
import datetime
import re
import codecs
import requests
import pandas as pd
import os
import fnmatch

import sys
sys.path.insert(0, "../Utilities")
import get_ticker_list
import config
from urllib.request import Request, urlopen


def get_google_finance_intraday(ticker, exchange, period=60, days=1):
    # build url
    url = 'https://finance.google.com/finance/getprices' + \
          '?p={days}d&f=d,o,h,l,c,v&q={ticker}&i={period}&x={exchange}'.format(ticker=ticker,
                                                                               period=period,
                                                                               days=days,
                                                                               exchange=exchange)
    #url = "https://finance.google.com/finance/getprices?p=50d&f=d,o,h,l,c,v&q=COX%26KINGS&i=300&x=NSE"

    page = requests.get(url)
    reader = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))
    columns = ['Close', 'High', 'Low', 'Open', 'Volume']
    rows = []
    times = []
    close_data = []
    for row in reader:
        if re.match('^[a\d]', row[0]):
            if row[0].startswith('a'):
                start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                times.append(start)
            else:
                times.append(start + datetime.timedelta(seconds=period * int(row[0])))
            rows.append(map(float, row[1:]))
    if len(rows):
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date Time'), columns=columns)
    else:
        return pd.DataFrame(rows, index=pd.DatetimeIndex(times, name='Date Time'))

def main():
    config_object = config.config("../config.txt")
    path_to_stock_master_list = config_object.path_to_master_list()
    path_to_historical_5_min_data = config_object.path_to_historical_5_min_dir()
    """Change folders here"""
    path_to_output_dir1 = config_object.path_to_output_dir() + "historical 5 min data/Final data/"
    path_to_output_dir2 = config_object.path_to_output_dir() + "historical 5 min data/Downloaded data/"
    ticker_list = get_ticker_list.get_ticker_list(path_to_stock_master_list)

    """Change the number of tickers here"""
    for ticker in ticker_list:

        """Change the granularity here"""
        # 300 for five minutes, 1800 for 30 minutes
        # last date for 5 minutes downloaded on June 19, 2018
        # last date for 30 minutes download on June 20, 2018
        # period = 300
        period = 1800
        days = 15
        exchange = 'NSE'
        print(ticker)
        if '_' in ticker:
            ticker = ticker[:ticker.index('_')] + "%26" + ticker[ticker.index('_') + 3:]
        df = get_google_finance_intraday(ticker, exchange, period=period, days=days)
        # if '%' in ticker:
        #     ticker = ticker[:ticker.index('%')] + "_26" + ticker[ticker.index('%') + 3:]
        df.to_csv(path_to_output_dir2 + ticker + ".csv")

    if len(fnmatch.filter(os.listdir(path_to_output_dir2), "*.csv")) == len(ticker_list):
        print("Downloaded Data Complete")

    for ticker in ticker_list:
        print(ticker)
        df = pd.read_csv(path_to_output_dir2 + ticker + ".csv", index_col=None)

        path_to_historical_data = path_to_historical_5_min_data + ticker + ".csv"

        df2 = pd.read_csv(path_to_historical_data, index_col=None)
        drop_index = []
        for i in df2.index:
            if "Close" in df2.values[i]:
                drop_index.append(i)
        if len(drop_index) > 0:
            df2 = df2.drop(df2.index[drop_index])

        last_value = df2.values[-1][0]
        last_index = -1
        for index in df.index:
            if df.values[index][0] == last_value:
                last_index = index
        if last_index == -1:
            df2 = df2.append(df)
        else:
            df = df.drop(df.index[:last_index + 1])
            df2 = df2.append(df)
        df2.to_csv(path_to_output_dir1 + ticker + ".csv", index=False)

    """Change according to the number of tickers"""
    if len(fnmatch.filter(os.listdir(path_to_output_dir1), "*.csv")) == len(ticker_list):
        print("Final Data Complete")
main()