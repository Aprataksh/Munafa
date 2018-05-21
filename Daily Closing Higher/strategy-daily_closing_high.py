import csv
import numpy
import math
import pandas as pd
import xlsxwriter

def resistance(ticker):
    df = pd.read_csv(r"C:/Users/Hp/Desktop/New folder/Top500_stock/Original data/" + ticker + ".csv")


    """Code to reduce the number of entries in stock data"""

    date_data = df['Date'].tolist()
    initial_data = "2018-04-10"
    index = 0
    for date in date_data:
        if initial_data in date:
            index = date_data.index(date)
            break
    if index == 0:
        print("no such date")
    else:
        df = df.drop(df.index[[range(0,index)]])


    """Code to extract day data from the 5 minute data we have"""

    date_data = df['Date'].tolist()
    close_data = df['Close'].tolist()
    open_data = df['Open'].tolist()
    low_data = df['Low'].tolist()
    open_day = []
    close_day = []
    date_day = []
    low_day = []
    open_day.append(open_data[0])
    date_day.append(date_data[0])
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
            date_day.append(date_data[i+1])
    for j in low_data[start_index:]:
        if j < min:
            min = j
    low_day.append(min)
    close_day.append(close_data[-1])

    """for i in range(1, len(date_day)):
        print(date_day[i], "\t", open_day[i], "\t", close_day[i], "\t", low_day[i])"""

    """Code to implement the stock trading strategy"""

    no_of_days = 3
    for i in range(1,len(date_day)-no_of_days+1):
        c = 0
        for j in range(0,no_of_days-1):
            if close_day[i+j] > open_day[i+j] and close_day[i+j-1] > open_day[i+j-1]:
                day_change = close_day[i+j-1]-open_day[i+j-1]
                if ((close_day[i+j-1] - open_day[i+j]) > .98 * day_change or open_day[i+j] > close_day[i+j-1]) and low_day[i+j] > open_day[i+j-1] :
                    c += 1
            if c == no_of_days-1:
                dates.append(((date_day[i+j-2][0:10], open_day[i+j-2], close_day[i+j-2], low_day[i+j-2]),
                              (date_day[i+j-1][:10], open_day[i+j-1], close_day[i+j-1], low_day[i+j-1]),
                              (date_day[i+j][:10], open_day[i+j], close_day[i+j], low_day[i+j])))

        if c == no_of_days-1:
            strategy_ticker.append(ticker)

ticker_list = []
strategy_ticker = []
dates = []
def get_ticker_list():
    with open(r"C:\Users\Hp\Desktop\New folder\nifty500_list.csv", 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                ticker_list.append(line[2])
        # print(ticker_list)

def main():
    get_ticker_list()
    for ticker in ticker_list[:10]:
        if '&' in ticker:
            ticker = ticker[:ticker.index('&')] + "%26" + ticker[ticker.index('&') + 1:]
        print(ticker)
        resistance(ticker)
    if len(strategy_ticker) == 0:
        print("No company followed such strategy ")
    else:
        c = 1
        for i in range(0, len(strategy_ticker) - 1):
            if strategy_ticker[i] != strategy_ticker[i + 1]:
                c = c + 1

        print("Strategy is followed by =", c, " companies\n")

        rows = zip(strategy_ticker, dates)
        with open(r"C:/Users/Hp/Desktop/New folder/Top500_stock/strategy1.csv", 'w') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

        """for i in range(0, len(strategy_ticker)):
            print(strategy_ticker[i], dates[i])"""

main()