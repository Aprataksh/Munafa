import csv
import math
import logging
from config import config
import sys
sys.path.insert(0, "../Utilities")
import get_ticker_list
import pandas as pd

def drop_data(ticker):

    # directory path to the historical data. Ensure that there is a / at the end
    config_object = config("../config.txt")
    path_to_historical_data = config_object.path_to_historical_5_min_dir()
    path_to_output_dir = config_object.path_to_output_dir()

    log_filename = "strategy_log.log"
    log_format = "%(levelname)s - %(message)s"
    logging.basicConfig(filename=path_to_output_dir+log_filename, level=logging.DEBUG, format=log_format, filemode="w")
    logger = logging.getLogger()

    df = pd.read_csv(path_to_historical_data + ticker + ".csv")

    """Remove any of the headers in the code"""

    drop_index = []         #contains all the indices where there is a header value
    for index in df.index:
        if "Close" in df.values[index]:
            drop_index.append(index)
    #dropping header values at the same time.
    df = df.drop(index=drop_index)

    """Code to reduce the number of entries in stock data"""
    date_data = df['Date Time'].tolist()

    """Converting values to float, so if there is a string in a column, an error will occur here"""

    df['Close'] = df['Close'].astype(float)
    df['Open'] = df['Open'].astype(float)
    df['Low'] = df['Low'].astype(float)

    initial_data = "2018-03-13"
    index = 0
    for date in date_data:
        if initial_data in date:
            index = date_data.index(date)
            break
    if index == 0:
        logger.info("No data on " + initial_data + " for " + ticker)
    else:
        logger.info("Dropped data from " + initial_data + " for " + ticker)
        df = df.drop(df.index[[range(0,index)]])
    return df


"""Code to extract day data from the 5 minute data we have"""
def get_daily_closing_high(no_of_days, output_folder):

    strategy_ticker = []
    dates = []

    """Config Object"""
    config_object = config("../config.txt")
    path_to_output_dir = config_object.path_to_output_dir() + output_folder

    path_to_stock_masterlist = config_object.path_to_master_list()
    ticker_list = get_ticker_list.get_ticker_list(path_to_stock_masterlist)

    output_filename = "scanner_output.csv"
    log_filename = "strategy_log.log"

    """Logging Details"""
    log_format = "%(levelname)s - %(message)s"
    logging.basicConfig(filename=path_to_output_dir + log_filename, level=logging.DEBUG, format=log_format, filemode="w")
    logger = logging.getLogger()
    for ticker in ticker_list:
        #Drops the data before the initial date
        df = drop_data(ticker)

        """List containing 5-min data"""

        date_data = df['Date Time'].tolist()
        close_data = df['Close'].tolist()
        open_data = df['Open'].tolist()
        low_data = df['Low'].tolist()

        """Code for the conversion of 5-min data to 1-day data"""

        open_day = []
        close_day = []
        date_day = []
        low_day = []

        open_day.append(open_data[0])
        date_day.append(date_data[0][:10])
        start_index = 0
        for i in range(0, len(date_data)-1):
            date = date_data[i][:10]
            next_date = date_data[i+1][:10]
            min = low_data[start_index]
            if date != next_date:
                end_index = i
                for j in low_data[start_index:end_index+1]:
                    if j < min:
                        min = j
                start_index = i+1
                low_day.append(min)
                close_day.append(close_data[i])
                open_day.append(open_data[i+1])
                date_day.append(date_data[i+1][:10])
        for j in low_data[start_index:]:
            if j < min:
                min = j
        low_day.append(min)
        close_day.append(close_data[-1])

        """Code to implement the stock trading strateg"""
        for i in range(1,len(date_day)-no_of_days+1):
            c = 0
            # Code Change: Add float to convert values from string
            for j in range(0,no_of_days-1):
                previous_day = i + j - 1
                current_day = i + j
                current_day = i + j
                previous_day = i + j - 1
                if float(close_day[current_day]) > float(open_day[current_day])\
                        and float(close_day[previous_day]) > float(open_day[previous_day]):
                    day_change = float(close_day[previous_day])-float(open_day[previous_day])
                    if ((float(close_day[previous_day]) - float(open_day[current_day])) > .98 * day_change
                        or float(open_day[current_day]) > float(close_day[previous_day]))\
                            and float(low_day[current_day]) > float(open_day[previous_day]) :
                        c += 1
                if c == no_of_days-1:
                    dates.append([ticker, date_day[i+j-2], date_day[previous_day], date_day[current_day], date_day[i+j+1]])
            if c == no_of_days-1:
                strategy_ticker.append(ticker)


    if len(dates) == 0:
        logger.error("No companies followed this strategy")
    else:
        c = 1
        for i in range(0, len(dates) - 1):
            if dates[i][0] != dates[i + 1][0]:
                c = c + 1

        logger.info("Strategy is followed by = " + str(c) + " companies")
        #rows = zip(strategy_ticker, dates)
        with open(path_to_output_dir + output_filename, 'w', newline="") as f:
            writer = csv.writer(f)
            for row in dates:
                writer.writerow(row)



def main():
    ndays = 3
    output_folder = "Strategy_daily_closing_higher/"
    get_daily_closing_high(ndays, output_folder)