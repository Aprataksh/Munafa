import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "../Utilities")
import get_ticker_list
import drop_extra_headers
from config import config

def macd_crossover(ticker,path_to_data):
    config_object = config("../config.txt")
    path_to_historical_data = path_to_data
    df = pd.read_csv(path_to_historical_data + ticker + ".csv")
    # FAST_EMA = pd.Series(round((df['Close']).ewm(span=12).mean(), 2), name="FAST_EMA")
    FAST_EMA = pd.Series(round((df['Close']).ewm(span=12,adjust=False).mean(), 2), name="FAST_EMA")
    SLOW_EMA = pd.Series(round((df['Close']).ewm(span=26,adjust=False).mean(), 2), name="SLOW_EMA")
    MACD_LINE = round(FAST_EMA - SLOW_EMA, 2)
    macd_list = MACD_LINE.tolist()
    date_time_list = df['Date Time'].tolist()
    fast_ema = FAST_EMA.tolist()
    # df.join(MACD_LINE)
    # print(df)
    for x in macd_list:
        x = round(x, 2)
    x = range(len(macd_list))

    SIGNAL_LINE = pd.Series(round(MACD_LINE.ewm(span=9, adjust=False).mean(), 2), name="SIGNAL_EMA")
    signal_list = SIGNAL_LINE.tolist()
    return macd_list, signal_list
"""
    print(macd_list, sep="\n")
    print(date_time_list, sep="\n")
    rows = zip(date_time_list, fast_ema,macd_list)
    path_to_output_directory = config_object.path_to_output_dir()
    with open(path_to_output_directory +  "Test Bajaj.csv", 'w',
              newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
        f.close()


"""
"""
    fig = plt.figure()
    "Slow and Fast EMA plot"

    plt.subplot(2, 1, 1)
    plt.plot(x, SLOW_EMA, '-')
    plt.plot(x, FAST_EMA, '-')
    plt.title(ticker)
    plt.legend(["SLOW EMA", "FAST EMA"])

    "MACD and Signal Line plot"

    plt.subplot(2, 1, 2)
    plt.plot(x, MACD_LINE)
    plt.plot(x, SIGNAL_LINE)
    plt.fill_between(x, MACD_LINE - SIGNAL_LINE, color='gray', alpha=0.5, label="MACD HISTOGRAM")
    plt.legend(["MACD LINE", "SIGNAL_LINE"])
    plt.grid()
    plt.show()
"""

def main():
    stdev_list = []
    config_object = config("../config.txt")
    filename = "ind_niftyfmcglist.csv"
    path_to_stock_masterlist = config_object.path_to_master_list()
    print(path_to_stock_masterlist, "\n")
    ticker_list = get_ticker_list.get_ticker_list(path_to_stock_masterlist)
    for ticker in ticker_list[:1]:
        macd_crossover(ticker)
        # print(ticker, "\n")

