'''
author: Aprataksh Anand
this provides a list of all that ticker symbols for stocks that need to be processed
'''
import csv

def get_ticker_list(path_to_stock_master_list):
    ticker_list = []
    with open(path_to_stock_master_list, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                if '&' in line[2]:
                    line[2] = line[2][:line[2].index('&')] + "_26" + line[2][line[2].index('&') + 1:]
                ticker_list.append(line[2])
    return ticker_list

'''
def main():
    ticker_list = get_ticker_list()

main()
'''