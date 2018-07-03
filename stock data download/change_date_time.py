import csv
import sys
sys.path.insert(0, "../Utilities")
from config import config
import get_ticker_list


def main():

    config_object = config("../config.txt")
    path_to_master_list = config_object.path_to_master_list()
    path_to_historical_data = config_object.path_to_historical_1_day_dir()
    path_to_output_dir = config_object.path_to_output_dir() + "Test 1 day-dir/"
    ticker_list = get_ticker_list.get_ticker_list(path_to_master_list)

    for ticker in ticker_list:
        if '_26' in ticker:
            ticker = ticker[:ticker.index('_')] + "&" + ticker[ticker.index('_') + 3:]
        print(ticker)
        with open(path_to_historical_data + ticker + ".csv", 'r') as infile:
            readstream = csv.reader(infile, delimiter=',')
            with open(path_to_output_dir + ticker + ".csv", 'w', newline="") as output:
                outwriter = csv.writer(output, delimiter=',')
                i = 0
                for row in readstream:
                    if i == 0:
                        i = 1
                        row[0] = "Date Time"
                    outwriter.writerow(row)
main()
