import csv
import pandas as pd
import get_ticker_list

def drop_headers_print_to_file():
    path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/nifty500_list.csv"
    path_to_historical_data = "C:/Users/Rohit/Python_source_code/historical_stock_5_min_data/"
    path_to_output_directory = r"C:\Users\Rohit\Python_source_code\sanitised data\historical_stock_5_min_data/"
    '''
    path_to_stock_master_list = r"C:/Users/Hp/Desktop/New folder/nifty500_list.csv"
    path_to_historical_data = r"C:/Users/Hp/Desktop/New folder/historical_stock_5_min_data/"
    path_to_output_directory = r"C:/Users/Hp/Desktop/New folder/Sanitized Data/Top500_stock/"
    '''
    ticker_list = get_ticker_list.get_ticker_list(path_to_stock_master_list)
    c = 0
    for ticker in ticker_list:

        c = c + 1
        print(ticker)
        df = pd.read_csv(path_to_historical_data + ticker + ".csv", index_col = False)
        drop_index = []
        for i in df.index:
            if "Close" in df.values[i]:
                drop_index.append(i)
        if len(drop_index) > 0:
            df = df.drop(df.index[drop_index])
        df.to_csv(path_to_output_directory + ticker + ".csv", index = False)
    if c == len(ticker_list):
        print("Every file has been replaced")
def main():
    drop_headers_print_to_file()
main()

