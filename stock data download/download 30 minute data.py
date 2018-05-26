'''
this code is based on the following post
http://dacatay.com/data-science/download-free-intraday-stock-data-from-google-finance-with-python/

the main differences are that we take care of any company  which has a & in its name and
the append the newly downloaded data to historical data give the appropriate flag has been
added in the source code. note that while appending, the headers of datetime, close high etc..
are also a appended.different approaches including reading the file into a pandas data frame or
using a csv reader and writer work tried to work around this. In the former case,  the pandas data frame
ends up prepending the row numbertto every row.  In the latter, the writer ends up adding a blank row.
So for now, we will live with multiple headers being a part of historical data
'''

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
'''
global configuration settings
'''
# interval in seconds  - for 5 minutes, use 60 seconds, for 15-900, for 30-1800, 60-3600
period = 1800
# number of days in the past for which to download data. Maximum seems to be 50
days = 1
# name of the exchange. For India, use NSE
exchange = 'NSE'
# should be appended the newly downloaded data in CSV files to historical data? Enter 1 for yes
append_to_historical_data = 1

# modify the directory path below according to your requirements
# Note: these directories should already be existing in your file system
path_to_historical_data = "C:/Users/Rohit/Python_source_code/historical_stock_30_min_data/"
path_to_cur_stock_data_directory = "C:/Users/Rohit/Python_source_code/current_stock_30_min_data/"

'''
# configuration for testing
path_to_historical_data = "C:/Users/Rohit/Python_source_code/test_nse 500 historical data/"
path_to_cur_stock_data_directory = "C:/Users/Rohit/Python_source_code/test_current_stock_data/"
'''
# the list that contains the symbols for all the stocks that need to be downloaded
path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/nifty500_list.csv"

get_ticker_list()
for ticker in ticker_list:
    if '&' in ticker:
        ticker = ticker[:ticker.index('&')] + "%26" + ticker[ticker.index('&') + 1:]
    print(ticker)
    df = get_google_finance_intraday(ticker, exchange, period=period, days=days)
    df.to_csv(path_to_cur_stock_data_directory + ticker + ".csv")

    if (append_to_historical_data == 1):
        with open(path_to_historical_data+ ticker + ".csv", 'a') as f:
            with open(path_to_cur_stock_data_directory + ticker + ".csv", 'r') as tempfile:
                f.write(tempfile.read())
            '''
            Using csv.reader and a writer along with the writerow does not work because
            while writing, and extra blank row is being added
            
            row_file_writer = csv.writer(f)
                lines = csv.reader(tempfile)
                for line in lines:
                    if "Close" not in line:
                        row_file_writer.writerow(line)
             '''

        '''
            when we read the data in the data frame, it also prepends every row with the row number
        '''
        '''    
        if (append_to_historical_data == 1):
            historical_df = pd.read_csv(path_to_historical_data + ticker + ".csv")
            appended_data = historical_df.append(df)
            appended_data.to_csv(path_to_historical_data + ticker + " backup2"+".csv")
        '''




