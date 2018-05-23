import csv
import datetime
import re
import codecs
import requests
import pandas as pd
import statistics
import math
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

ticker_list = []
def get_ticker_list():
    with open(path_to_stock_master_list, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                ticker_list.append(line[2])
        print(ticker_list)

adj_list = []

period = 300
days = 2
exchange = 'NSE'
append_to_historical_data = 1
path_to_historical_data = "C:/Users/Rohit/Python_source_code/test_nse 500 historical data/"
path_to_cur_stock_data_directory = "C:/Users/Rohit/Python_source_code/current_stock_data/"
path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/nse 500 stock data/test_nifty500_list.csv"

get_ticker_list()
for ticker in ticker_list:
    if '&' in ticker:
        ticker = ticker[:ticker.index('&')] + "%26" + ticker[ticker.index('&') + 1:]
    print(ticker)
    df = get_google_finance_intraday(ticker, exchange, period=period, days=days)
    df.to_csv(path_to_cur_stock_data_directory + ticker + ".csv")
    if (append_to_historical_data == 1):
        historical_df = pd.read_csv(path_to_historical_data+ ticker + ".csv")
        historical_df.append(df)
        historical_df.to_csv(path_to_historical_data+ ticker + ".csv")
        '''
        with open(path_to_historical_data+ ticker + ".csv", 'a') as f:
            with open(path_to_cur_stock_data_directory + ticker + ".csv", 'r') as tempfile:
                row_file_writer = csv.writer(f)
                lines = csv.reader(tempfile)
                for line in lines:
                    if "Close" not in line:
                        row_file_writer.writerow(line)
                #f.write(tempfile.read())
                '''


