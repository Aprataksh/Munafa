'''
calculate the resistance by looking aat the price range in which a particular security has
spent the maximum amount of time. the number of ranges and the frequency  for every stock is provided as an output
'''
import csv
import numpy
import math
import pandas as pd
import xlsxwriter

def resistance(ticker):
    df = pd.read_csv(path_to_historical_data + ticker + ".csv")
    if len(df.columns) >= 6:
        high_data = (df['High']).tolist()
        maxi = math.ceil(max(high_data))
        mini = math.floor(min(high_data))
        interval = numpy.around(numpy.linspace(mini, maxi, no_of_intervals+1), 2).tolist()
        interval_data = []
        nmax = 0
        maxpos = mini
        for i in interval[:-1]:
            c = 0
            for j in high_data:
                if j >= i and j < (interval[interval.index(i) + 1]):
                    c = c + 1
            if c > nmax:
                nmax = c
                maxpos = i
            if (c != 0):
                interval_data.append((i, interval[interval.index(i) + 1], c))
            else:
                interval_data.append((i, interval[interval.index(i) + 1], 0))

        interval_data.append((maxpos, interval[interval.index(maxpos) + 1], nmax))
        intervals_data.append(interval_data)
        new_ticker_list.append(ticker)

ticker_list = []
high_data = []
max_list= []
intervals_data = []
no_of_intervals = 10
columns = []
new_ticker_list = []

'''
global configuration settings
'''
# modify the directory path below according to your requirements
# Note: these directories should already be existing in your file system
path_to_historical_data = "C:/Users/Rohit/Python_source_code/current_stock_5_min_data/"
# the list that contains the symbols for all the stocks that need to be downloaded
path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/nifty500_list.csv"
path_to_output = "C:/Users/Rohit/Python_source_code/Munafa/Resistance/resistance3.csv"

for i in range(1,no_of_intervals+1):
    columns.append("INTERVAL NO. " + str(i))
columns.append("MAX FREQ.")
def get_ticker_list():
    with open(path_to_stock_master_list, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                ticker_list.append(line[2])
        # print(ticker_list)

def main():
    get_ticker_list()
    for ticker in ticker_list:
        if '&' in ticker:
            ticker = ticker[:ticker.index('&')] + "%26" + ticker[ticker.index('&') + 1:]
        print(ticker)
        resistance(ticker)

    sdf = pd.DataFrame(intervals_data, index=pd.Series(new_ticker_list, name="SYMBOL"), columns=columns)
    """SAVING IN CSV"""
    sdf.to_csv(path_to_output)
    '''SAVING IN XLSX
    writer = pd.ExcelWriter(r"C:/Users/Hp/Desktop/New folder/Top500_stock/resistance.xlsx", engine="xlsxwriter")
    sdf.to_excel(writer, sheet_name="Sheet1")
    writer.save()
    '''
main()