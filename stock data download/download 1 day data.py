from googlefinance.client import get_price_data
import sys
sys.path.insert(0, r"..\utilities")
import get_ticker_list
import config

# Dow Jones

obj = config.config(r"../config.txt")
def main():
    ticker_list=get_ticker_list.get_ticker_list(obj.path_to_master_list())
    path=obj.path_to_output_dir()+"Historical_data_1_day/"
    for ticker in ticker_list:
        param = {
            'q': ticker,  # Stock symbol (ex: "AAPL")
            'i': "86400",  # Interval size in seconds ("86400" = 1 day intervals)
            'x': "NSE",  # Stock exchange symbol on which stock is traded (ex: "NASD")
            'p': "50d"  # Period (Ex: "1Y" = 1 year)
        }
        # get price data (return pandas dataframe)
        df = get_price_data(param)
        df.index.name="Date Time"
        df = df[['Close', 'High', 'Low', 'Open', 'Volume']]
        df.to_csv(path+ticker+".csv")
        print(ticker)

main()
