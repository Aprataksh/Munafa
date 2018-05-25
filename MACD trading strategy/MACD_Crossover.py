import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def get_values(ticker):
    df = pd.read_csv(path_to_historical_data + ticker + ".csv")

    """Code to reduce the number of entries in stock data"""

    date_data = df['Date Time'].tolist()
    #initial_data = "2018-05-10"
    index = 0
    for date in date_data:
        if initial_data in date:
            index = date_data.index(date)
            break
    if index == 0:
        print("no such date")
    else:
        df = df.drop(df.index[[range(0,index)]])
    return df

def get_ticker_list():
    with open(path_to_stock_master_list, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                ticker_list.append(line[2])

ticker_list = []

'''
global configuration settings
'''
# modify the directory path below according to your requirements
# Note: these directories should already be existing in your file system
path_to_historical_data = "C:/Users/Rohit/Python_source_code/current_stock_5_min_data/"
# the list that contains the symbols for all the stocks that need to be downloaded
path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/test_single_nifty500_list.csv"
# determine the timestamp to append to the nname of the output file
time=str(datetime.datetime.today())[:13]+";"+str(datetime.datetime.today())[14:16]
path_to_output = "C:/Users/Rohit/Python_source_code/Munafa/Resistance/resistance4 ; " + time + ".csv"

# the initial date from which we need to start processing the data.
# make sure that this date falls on a trading  day.
initial_data = "2018-05-21"
# number of intervals in which the price range will be divided. the larger the number,the more accurate the information

def main():
    stdev_list = []
    get_ticker_list()
    for ticker in ticker_list[:3]:
        df = get_values(ticker)
        print(ticker, "\n")
        FAST_EMA = pd.Series(round((df['Close']).ewm(span=12).mean(), 2), name="FAST_EMA")
        SLOW_EMA = pd.Series(round((df['Close']).ewm(span=26).mean(), 2), name="SLOW_EMA")

        MACD_LINE = round(SLOW_EMA - FAST_EMA, 2)
        macd_list = MACD_LINE.tolist()
        for x in macd_list:
            x = round(x, 2)
        x = range(0, len(macd_list))

        SIGNAL_LINE = pd.Series(round(MACD_LINE.ewm(span=9).mean(), 2), name="SIGNAL_EMA")
        signal_list = SIGNAL_LINE.tolist()

        fig = plt.figure()
        "Slow and Fast EMA plot"

        plt.subplot(2, 1, 1)
        plt.plot(x, SLOW_EMA, '-')
        plt.plot(x, FAST_EMA, '-')
        plt.suptitle(ticker)
        plt.legend(["SLOW EMA", "FAST EMA"])

        "MACD and Signal Line plot"

        plt.subplot(2, 1, 2)
        plt.plot(x, MACD_LINE)
        plt.plot(x, SIGNAL_LINE)
        plt.fill_between(x, MACD_LINE - SIGNAL_LINE, color='gray', alpha=0.5, label="MACD HISTOGRAM")
        plt.legend(["MACD LINE", "SIGNAL_LINE"])
        plt.grid()
        plt.show()

        for i in x[1:]:

            """Condition for about to cross_above"""

            if macd_list[i] > macd_list[i - 1] and signal_list[i] > macd_list[i]:
                if macd_list[i] - macd_list[i - 1] > signal_list[i] - signal_list[i - 1]:
                    print("BUY At i = ", i, df['Date Time'].tolist()[i], macd_list[i], signal_list[i])

            """Condition for cross_above"""

            if macd_list[i] > signal_list[i] and macd_list[i - 1] < signal_list[i - 1]:
                print("Crossed Above Signal Line ", "Before = ", macd_list[i - 1], signal_list[i - 1],
                      "After = ", macd_list[i], signal_list[i])

            """Condition for about to cross_below"""

            if macd_list[i] < macd_list[i - 1] and signal_list[i] < macd_list[i]:
                if macd_list[i - 1] - macd_list[i] > signal_list[i - 1] - signal_list[i]:
                    print("SELL At i = ", i, df['Date Time'].tolist()[i], macd_list[i], signal_list[i])

            """Condition for cross_below"""

            if macd_list[i] < signal_list[i] and macd_list[i - 1] > signal_list[i - 1]:
                print("Crossed Below Signal Line ", "Before = ", macd_list[i - 1], signal_list[i - 1],
                      "After = ", macd_list[i], signal_list[i])


main()
