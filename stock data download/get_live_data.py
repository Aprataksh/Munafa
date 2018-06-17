import csv
import datetime
import codecs
import requests
import pandas as pd
from urllib.request import Request, urlopen
import sys
sys.path.insert(0, r"C:\Users\Hp\PycharmProjects\Utilities")
import drop_index
import drop_data
import get_ticker_list


class class_Data_source():
    def __init__(self, ticker, exchange, period, days):
        self.ticker = ticker
        self.exchange = exchange
        self.period = period
        self.days = days
        self.data_list = []
        self.columns=["Date Time", "Close", "High", "Low", 'Open', "Volume"]
        self.data_frame = pd.DataFrame(columns=self.columns)

    def get_live_data(self):
        url = 'https://finance.google.com/finance/getprices' + \
              '?p={days}d&f=d,o,h,l,c,v&q={ticker}&i={period}&x={exchange}'.format(ticker = self.ticker,
                                                                                   period = self.period,
                                                                                   days = self.days,
                                                                                   exchange = self.exchange)
        #url = "https://finance.google.com/finance/getprices?p=1d&f=d,o,h,l,c,v&q=3MINDIA&i=300&x=NSE"
        while (True):
            page1 = requests.get(url)
            reader1 = list(csv.reader(codecs.iterdecode(page1.content.splitlines(), "utf-8")))
            if len(self.data_list) == 0:
                for row in reader1:
                    if row[0].startswith('a'):
                        start_index = reader1.index(row)
                        start = datetime.datetime.fromtimestamp(int(row[0][1:]))
                        start_data = row
                        start_data[0] = str(start)
                        break
                self.data_list.append(start_data)
                self.data_frame = self.data_frame.append(pd.Series(start_data, index=self.columns), ignore_index = True)
                last_date = str(start)
                print("Intial Row = ", self.data_frame)


            for row in reader1[start_index + len(self.data_list):]:
                row[0] = str(start + datetime.timedelta(seconds=self.period * int(row[0])))
                self.data_list.append(row)
                self.data_frame = self.data_frame.append(pd.Series(row, index=self.columns), ignore_index = True)

                """Change file name here"""

                self.data_frame.to_csv(self.ticker + ".csv", index = False)

            print("Final Frame = ", self.data_frame)

    def get_data_list(self):
        return self.data_list
    def get_data_frame(self):
        return self.data_frame

def main():
    period = 300
    days = 1
    exchange = "NSE"
    ticker = "3MINDIA"
    data = class_Data_source(ticker, exchange, period=period, days=days)
    data.get_live_data()



main()