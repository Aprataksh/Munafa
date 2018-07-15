'''
calculate the resistance by looking aat the price range in which a particular security has
spent the maximum amount of time. the number of ranges and the frequency  for every stock is provided as an output
'''
import csv
import numpy
import math
import pandas as pd
import sys
sys.path.insert(0, "../Utilities")
from config import config
import get_ticker_list
import datetime

# Flag for 1 = resistance or 0 = support
flag_val = 0


def flag():
    if flag_val == 1:
        return 1
    else:
        return 0


def resistance(ticker):
    df = pd.read_csv(path_to_historical_data + ticker + ".csv")

    """CODE TO GET INDEX FOR DATA AFTER INITIAL DATE"""

    date_data = df['Date Time'].tolist()
    initial_index = 0
    for date in date_data:
        if initial_date in date:
            initial_index = date_data.index(date)
            break
    if initial_index == 0:
        print("No data present for such date")
    else:
        df = df.drop(df.index[[range(0, initial_index)]])

        """CODE TO CALCULATE RESISTANCE"""

    if len(df.columns):
        if flag() == 1:
            data = df['High'].tolist()
        else:
            data = df['Low'].tolist()
        maxi = math.ceil(max(data))
        mini = math.floor(min(data))
        interval = numpy.around(numpy.linspace(mini, maxi, no_of_intervals+1), 2).tolist()
        interval_data = [ticker]
        nmax = 0
        maxpos = mini
        for i in interval[:-1]:
            c = 0
            for j in data:
                if i <= j < interval[interval.index(i) + 1]:
                    c = c + 1
            if c > nmax:
                nmax = c
                maxpos = i

            interval_data.append((i, interval[interval.index(i) + 1], c))
        interval_data.append(maxpos)
        interval_data.append(interval[interval.index(maxpos) + 1])
        return interval_data

'''
global configuration settings
'''
# modify the directory path below according to your requirements
# Note: these directories should already be existing in your file system
# path_to_historical_data = "C:/Users/Rohit/Python_source_code/current_stock_5_min_data/"
# the list that contains the symbols for all the stocks that need to be downloaded
# path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/nifty500_list.csv"

# Config Object created
config_object = config("../config.txt")
path_to_stock_master_list = config_object.path_to_master_list()
path_to_historical_data = config_object.path_to_historical_5_min_dir()

# determine the timestamp to append to the name of the output file
time = str(datetime.datetime.today())[:13] + ";" + str(datetime.datetime.today())[14:16]
path_to_output = config_object.path_to_output_dir() + time + ".csv"

# the initial date from which we need to start processing the data.
# make sure that this date falls on a trading  day.
initial_date = "2018-05-21"
# number of intervals in which the price range will be divided. the larger the number,the more accurate the information
no_of_intervals = 10

# Creating the columns for the intervals
columns = ["TICKER"]
for i in range(1, no_of_intervals+1):
    columns.append("INTERVAL NO. " + str(i))
columns.append("LOW RANGE")
columns.append("HIGH RANGE")

# Creating a new file
with open(path_to_output, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(columns)


def main():
    ticker_list = get_ticker_list.get_ticker_list(path_to_stock_master_list)
    for ticker in ticker_list:
        if '&' in ticker:
            ticker = ticker[:ticker.index('&')] + "_26" + ticker[ticker.index('&') + 1:]
        print(ticker)
        interval_line = resistance(ticker)

        # Appending to the new file created
        with open(path_to_output, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(interval_line)


main()