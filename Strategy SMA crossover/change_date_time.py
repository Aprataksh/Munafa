import csv

def get_ticker_list():
    with open(r"C:\Users\Rohit\Python_source_code\nse 500 stock data\nifty500_list.csv", 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                ticker_list.append(line[2])

ticker_list = []
def main():
    stdev_list = []
    get_ticker_list()
    for ticker in ticker_list:
        if '&' in ticker:
            ticker = ticker[:ticker.index('&')] + "%26" + ticker[ticker.index('&') + 1:]
        print(ticker)
        with open(r"C:/Users/Rohit/Python_source_code/nse 500 stock data/" + ticker +".csv", 'r') as infile:
            readstream = csv.reader(infile, delimiter=',')
            with open(r"C:/Users/Rohit/Python_source_code/nse 500 stock data/Date Time Data/" + ticker +".csv", 'wt') as output:
                outwriter = csv.writer(output, delimiter=',')
                i = 0
                for row in readstream:
                    if i == 0:
                        i=1
                        row[0] = "Date Time"
                    outwriter.writerow(row)


main()
