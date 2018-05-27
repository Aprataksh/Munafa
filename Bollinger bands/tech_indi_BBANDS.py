'''
author: Aprataksh Anand
'''
 # Load the necessary packages and modules
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, r"..\utilities")
import get_ticker_list
import sanitise_data

# Compute the Bollinger Bands
def BBANDS(data, window=50):
    MA = data.Close.rolling(window=window).mean()
    SD = data.Close.rolling(window=window).std()
    data['UpperBB'] = MA + (2 * SD)
    data['LowerBB'] = MA - (2 * SD)
    return data

def main():
    # modify the directory path below according to your requirements
    # Note: these directories should already be existing in your file system

    # path to the list that contains the symbols for all the stocks that need to be downloaded
    path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/nifty500_list.csv"
    # path to the directory that contains all the historical data
    path_to_historical_data = "C:/Users/Rohit/Python_source_code/historical_stock_5_min_data/"
    # date before which we are not going to process the data
    date = "2018-04-10"

    ticker_list = get_ticker_list.get_ticker_list(path_to_stock_master_list)
    for ticker in ticker_list[:2]:
        # Sanitise the data
        # At this stage, we are removing any extra  headers  (which can be  added during that downloading process)
        # also remove all the data  that is before the user specified date
        data = sanitise_data.sanitise_data(path_to_historical_data, ticker, date)

        # Compute the Bollinger Bands for NIFTY using the 50-day Moving average
        n = 50
        NIFTY_BBANDS = BBANDS(data, n)
        print(NIFTY_BBANDS)

        # Create the plot
        pd.concat([NIFTY_BBANDS.Close, NIFTY_BBANDS.UpperBB, NIFTY_BBANDS.LowerBB], axis=1).plot(figsize=(9, 5),
                                                                                                  grid=True)
        plt.title(ticker)
        plt.show()


main()