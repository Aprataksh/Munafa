import csv
import math
import pandas as pd

def get_ticker_list():
    ticker_list = []
    #path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/ind_niftyfmcglist.csv"
    #path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/modified_ind_nifty50list.csv"
    path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/nifty500_list.csv"
    with open(path_to_stock_master_list, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                if '&' in line[2]:
                    line[2] = line[2][:line[2].index('&')] + "%26" + line[2][line[2].index('&') + 1:]
                ticker_list.append(line[2])
        return ticker_list

def drop_data(ticker):
    # directory path to the historical data. Ensure that there is a / at the end
    path_to_historical_data = "C:/Users/Rohit/Python_source_code/historical_stock_5_min_data/"

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
        print(ticker, " : no such date")
    else:
        df = df.drop(df.index[[range(0,index)]])
    return df


"""Code to extract day data from the 5 minute data we have"""
def get_daily_closing_high(no_of_days):

    strategy_ticker = []
    dates = []
    ticker_list = get_ticker_list()
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
    """If just the tickers then"""
    #return strategy_ticker, dates
    """If tickers with dates are needed"""
    #return dates
    if len(dates) == 0:
        print("No company followed such strategy ")
    else:
        c = 1
        for i in range(0, len(dates) - 1):
            if dates[i][0] != dates[i + 1][0]:
                c = c + 1

        print("Strategy is followed by =", c, " companies\n")

        #rows = zip(strategy_ticker, dates)
        with open("C:/Users/Rohit/Python_source_code/output/OHL/version2/daily_closing_higher_output.csv", 'w', newline = "") as f:
            writer = csv.writer(f)
            for row in dates:
                writer.writerow(row)



def main():
    ndays = 3
    get_daily_closing_high(ndays)