from googlefinance.client import get_price_data
import pandas as pd
import os, fnmatch
import sys
sys.path.insert(0, r"..\utilities")
import get_ticker_list
import config
import argparse, datetime

obj = config.config(r"../config.txt")
def main():
    # Extracting arguments from command line
    parser = argparse.ArgumentParser(description="download data")
    parser.add_argument("seconds", type=int, help="Number of seconds")
    parser.add_argument("days", type=int, help="Number of days")

    args = parser.parse_args()
    sec = args.seconds
    day = args.days

    # Names for the directory
    date = str(datetime.datetime.today())[:10]
    path_to_final_data = obj.path_to_output_dir() + "final data " + str(sec) + " " + date + "/"
    path_to_downloaded_data = obj.path_to_output_dir() + "downloaded data " + str(sec) + " " + date + "/"

    # Making required directory
    os.makedirs(path_to_final_data, exist_ok=True)
    os.makedirs(path_to_downloaded_data, exist_ok=True)

    # Condition for whether input seconds data exists or not
    if sec == 300:
        path_to_historical_data = obj.path_to_historical_5_min_dir()
    elif sec == 1800:
        path_to_historical_data = obj.path_to_historical_30_min_dir()
    elif sec == 86400:
        path_to_historical_data = obj.path_to_historical_1_day_dir()
    else:
        print("No such stock data present")
        exit(-1)

    ticker_url = ""
    ticker_list = get_ticker_list.get_ticker_list(obj.path_to_master_list())
    for ticker in ticker_list:
        if "_26" in ticker:
            ticker_url = ticker[:ticker.index('_')] + "&" + ticker[ticker.index('_')+3:]
        else:
            ticker_url = ticker

        param = {
            'q': ticker_url,  # Stock symbol (ex: "AAPL")
            'i': str(sec),  # Interval size in seconds ("86400" = 1 day intervals)
            'x': "NSE",  # Stock exchange symbol on which stock is traded (ex: "NASD")
            'p': str(day) + "d"  # Period (Ex: "1Y" = 1 year)
        }
        # get price data (return pandas dataframe)
        df = get_price_data(param)
        df.index.name = "Date Time"
        df = df[['Close', 'High', 'Low', 'Open', 'Volume']]
        df.to_csv(path_to_downloaded_data + ticker + ".csv")
        if len(df.index) == 0:
            print("Error : No data online")
        print(ticker_url)

    if len(fnmatch.filter(os.listdir(path_to_downloaded_data), "*.csv")) == len(ticker_list):
        print("Downloaded Data Complete")

    for ticker in ticker_list:
        if "_26" in ticker:
            ticker_url = ticker[:ticker.index('_')] + "&" + ticker[ticker.index('_') + 3:]
        else:
            ticker_url = ticker

        df = pd.read_csv(path_to_downloaded_data + ticker + ".csv", index_col=None)
        df2 = pd.read_csv(path_to_historical_data + ticker + ".csv", index_col=None)
        if "Date Time" not in df2.columns:
            df2.columns = ['Date Time', 'Close', 'High', 'Low', 'Open', 'Volume']
        df2 = df2[['Date Time', 'Close', 'High', 'Low', 'Open', 'Volume']]
        drop_index = []
        for i in df2.index:
            if "Close" in df2.values[i]:
                drop_index.append(i)
        if len(drop_index) > 0:
            df2 = df2.drop(df2.index[drop_index])

        if len(df2.index) != 0:
            last_value = df2.values[-1][0]
            last_index = -1
            for index in df.index:
                if df.values[index][0] == last_value:
                    last_index = index
            if last_index == -1:
                df2 = df2.append(df)
            else:
                df = df.drop(df.index[:last_index + 1])
                df2 = df2.append(df)
        else:
            print("Error : NO data in repository")
            df2 = df
        df2.to_csv(path_to_final_data + ticker + ".csv", index=False)
        print(ticker_url)

    """Change according to the number of tickers"""
    if len(fnmatch.filter(os.listdir(path_to_final_data), "*.csv")) == len(ticker_list):
        print("Final Data Complete")


main()