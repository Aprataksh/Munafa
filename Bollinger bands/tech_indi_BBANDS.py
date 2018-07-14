'''
author: Aprataksh Anand
'''
 # Load the necessary packages and modules
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, r"..\utilities")
import get_ticker_list
import config
import sanitise_data

config_obj = config.config(r"../config.txt")
# Compute the Bollinger Bands
def BBANDS(data, window):
    MA = data['Close'].rolling(window=window).mean()
    SD = data.Close.rolling(window=window).std()
    data['UpperBB'] = MA + (2 * SD)
    data['LowerBB'] = MA - (2 * SD)
    return data

def main(path, period, ticker):
    # modify the directory path below according to your requirements
    # Note: these directories should already be existing in your file system

    # path to the list that contains the symbols for all the stocks that need to be downloaded
    path_to_stock_master_list = config_obj.path_to_master_list()
    # path to the directory that contains all the historical data
    path_to_historical_data = path
    data = pd.read_csv(path_to_historical_data + ticker + ".csv")
    # Compute the Bollinger Bands for NIFTY using the 50-day Moving average
    NIFTY_BBANDS = BBANDS(data, period)
    return NIFTY_BBANDS

    '''
    # Create the plot
    pd.concat([NIFTY_BBANDS.Close, NIFTY_BBANDS.UpperBB, NIFTY_BBANDS.LowerBB], axis=1).plot(figsize=(9, 5),
                                                                                                grid=True)
    plt.title(ticker)
    plt.show()
    '''
main(config_obj.path_to_historical_1_day_dir(), 2, "3MINDIA")
