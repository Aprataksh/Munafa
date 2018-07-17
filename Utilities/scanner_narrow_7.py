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
    path_to_historical_data = config_object.path_to_historical_1_day_dir()
    path_to_output_dir = config_object.path_to_output_dir()

    log_filename = "strategy_log.log"
    log_format = "%(levelname)s - %(message)s"
    logging.basicConfig(filename=path_to_output_dir + log_filename, level=logging.DEBUG, format=log_format, filemode="w")
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
    logger.info("scanning for daily closing higher from date: " + initial_data)
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
def get_narrow_7(ndays, output_folder):

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

        date_day = df['Date Time'].tolist()
        close_day = df['Close'].tolist()
        open_day = df['Open'].tolist()
        low_day = df['Low'].tolist()

        logger.info(ticker)
        """Code to implement the stock trading strateg"""
        for i in range(0,len(date_day) - ndays + 1):
            c = 0
            range_list = []
            date_list = [ticker]
            # Code Change: Add float to convert values from string
            for j in range(i,i + ndays):
                range_value = abs( close_day[j] - open_day[j] )
                range_list.append(range_value)
                logger.debug(date_day[j][:10]+" "+str(range_value))
            if j+1 < len(date_day) - 1:
                range_value = abs(close_day[j+1] - open_day[j+1])
                logger.debug(date_day[j+1][:10]+" "+str(range_value))
                if range_value < min(range_list):
                    date_list.append(date_day[j+1][:10])
                    date_list.append(date_day[j+2][:10])
                    dates.append(date_list)
            logger.debug("\n")
        with open(path_to_output_dir + output_filename, 'w', newline="") as f:
            writer = csv.writer(f)
            for row in dates:
                writer.writerow(row)
def main():
    ndays = 7
    output_folder = "Narrow7/"
    get_narrow_7(ndays, output_folder)
