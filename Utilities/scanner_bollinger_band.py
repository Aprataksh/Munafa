import csv
import math
import logging
from config import config
import sys
sys.path.insert(0, "../Utilities")
import get_ticker_list
import pandas as pd
sys.path.insert(1, "../Bollinger bands")
import tech_indi_BBANDS

def drop_data(ticker):

    # directory path to the historical data. Ensure that there is a / at the end
    config_object = config("../config.txt")
    path_to_historical_data = config_object.path_to_historical_1_day_dir()
    path_to_output_dir = config_object.path_to_output_dir()

    log_filename = "strategy_log.log"
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=path_to_output_dir + log_filename,
                        level=logging.DEBUG, format=log_format,
                        datefmt='%Y-%m-%d', filemode="w")
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
def BB_Scanner(ndays, period, output_folder, threshold):

    strategy_ticker = []
    dates = []
    skip_ticker = False

    """Config Object"""
    config_object = config("../config.txt")
    path_to_output_dir = config_object.path_to_output_dir() + output_folder

    path_to_stock_masterlist = config_object.path_to_master_list()
    ticker_list = get_ticker_list.get_ticker_list(path_to_stock_masterlist)

    output_filename = "scanner_output.csv"
    log_filename = "strategy_log.log"

    """Logging Details"""
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=path_to_output_dir + log_filename,
                        level=logging.DEBUG, format=log_format,
                        datefmt='%Y-%m-%d', filemode="w")
    logger = logging.getLogger()
    for ticker in ticker_list:
        #Drops the data before the initial date
        print(ticker)
        df = drop_data(ticker)
        df = tech_indi_BBANDS.main(config_object.path_to_historical_1_day_dir(), period, ticker)
        per_ba = (df['Close'] - df['LowerBB']) / (df['UpperBB'] - df['LowerBB'])
        """List containing 5-min data"""

        date_day = df['Date Time'].tolist()
        logger.info(ticker)
        """Code to implement the stock trading strateg"""
        for i in range(period -1 ,len(date_day) - ndays + 1):
            date_list = []
            date_list.append(ticker)
            for j in range(i, i + ndays):
                if per_ba[j] < threshold:
                    if per_ba[j] < -10:
                        skip_ticker = True
                        logger.info("The value of %b dropped below -10. Some problem in data. Moving to next stock")
                        break
                    logger.debug("Value = " + str(per_ba[j]) + " on date " + date_day[j] + " for ticker " + ticker)
                    date_list.append(date_day[j][:10])
                else:
                    break
            if skip_ticker == True:
                skip_ticker = False
                break
            if len(date_list) == ndays + 1:
                if j+1 <= len(date_day) - 1:
                    logger.debug("Value = " + str(per_ba[j+1]) + " on date " + date_day[j+1] + " for ticker " + ticker)
                    date_list.append(date_day[j+1][:10])
                    dates.append(date_list)
    with open(path_to_output_dir + output_filename, 'w', newline="") as f:
        writer = csv.writer(f)
        for row in dates:
            writer.writerow(row)
def main():
    ndays = 3
    period = 5
    output_folder = "BB_Scanner/"
    threshold = 0.5
    BB_Scanner(ndays, period, output_folder, threshold)

# main()
