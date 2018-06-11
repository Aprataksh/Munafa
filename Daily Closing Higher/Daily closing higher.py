import csv
import sys
import pandas as pd
import logging
sys.path.insert(0, r"..\utilities")
import is_index_in_same_direction
import strategy_daily_closing_high
import config
from transaction import transaction


class DCH():
    obj = config.config(r"../config.txt")
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=obj.path_to_output_dir() + "Daily_closing_higher/dch_log.Log", level=logging.DEBUG,
                        format=LOG_FORMAT, filemode='w')
    logger = logging.getLogger()

    rowslist = []
    line = []
    total_cost = 0.0
    total_sell = 0.0
    total_purchased = 0
    total_sold = 0
    overall_cost = 0.0
    overall_sell = 0.0
    overall_c_wins = 0
    overall_c_stoploss = 0
    overall_c_sellEod = 0
    c_total_sellEOD = 0
    c_total_wins = 0
    c_total_stoploss = 0
    c_overall_buy_trans = 0
    column_no_of_ticker = 0

    # column_no_of_ticker = 2
    def __init__(self, dfpc, mpv, mdfo, mvv, mcfsb, tp, sl, mns):
        self.deviation_from_prev_close = dfpc
        self.max_price_volatility = mpv
        self.max_deviation_from_open = mdfo
        self.max_volume_volatility = mvv
        self.max_capital_for_single_buy = mcfsb
        self.target_price = tp
        self.stop_loss = sl
        self.recorded_date = []
        self.day_open_price = []
        self.max_ndays_scan = mns
        tf = open(self.obj.path_to_output_dir() + "Daily_closing_higher/transactions.csv", 'w', newline="")
        self.transactions_file = csv.writer(tf)

    def new_output_row(self):
        self.recorded_date.append("0")
        self.day_open_price.append("0")
        self.buy_amount.append("0")
        self.sell_amount.append("0")
        self.index_in_same_direction.append("0")
        self.sell_stop_loss.append("0")
        self.sell_EOD.append("0")
        self.buy_transaction.append("0")
        self.sell_met_target.append("0")
        self.rejected_price.append("0")
        self.rejected_volume.append("0")

    def buy_stocks(self, purchase_cost, index_close):

        bought = int(self.max_capital_for_single_buy / purchase_cost)
        if bought != 0:
            actual_cost = (bought * purchase_cost)
            self.total_cost = self.total_cost + actual_cost
            self.total_purchased += bought
            self.overall_cost = self.overall_cost + actual_cost
            self.c_overall_buy_trans = self.c_overall_buy_trans + 1
            self.c_transactions_today = self.c_transactions_today + 1
            self.buy_amount[-1] = str(actual_cost)
            self.logger.info("Stock " + self.line[0] + " bought " + str(bought) + " shares at " + str(
                purchase_cost) + " price at date " + str(self.rowslist[index_close])[2:12] + " at time " + str(
                self.rowslist[index_close])[12:18] + "\n")

            """Use of Transaction Class"""
            date = str(self.rowslist[index_close])[2:12]
            time = str(self.rowslist[index_close])[12:18]
            print_object = transaction(self.path_to_transaction_file)
            print_object.print_transaction_items(date, time, self.line[0], "1", str(bought), str(purchase_cost),
                                                 str(actual_cost), "0")

            '''
            self.transactions_file.writerow(str(self.rowslist[index_close])[2:12] +  str(self.rowslist[index_close])[12:18] +
                                            self.line[0] +  "1" +  str(bought) + str(purchase_cost) + str(0.0-actual_cost) +
                                            "0")
            '''
        else:
            # this may happen if the price of one stock is more than the  maximum capital
            self.logger.error("Could not buy stock " + self.line[0] + " on date " + str(self.rowslist[index_close])[
                                                                                    2:12] + " due to insufficient daily stock fund\n")
        return bought

    def sell_stock_due_to_price_check(self, bought, close_price, index):
        per = (float(self.rowslist[index][2]) - close_price) / close_price
        if per >= self.target_price:
            sell_amount = bought * float(self.rowslist[index][2])
            self.total_sell = self.total_sell + sell_amount
            self.overall_sell = self.overall_sell + sell_amount
            self.total_sold += bought
            self.logger.info("Stock " + self.line[0] + " sold " + str(bought) + " shares at " + self.rowslist[index][
                2] + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[
                                                                                         13:18] + "\n")
            self.overall_c_wins = self.overall_c_wins + 1
            self.c_total_wins = self.c_total_wins + 1
            # the last element has already been initialised to  0.  modify it to the sold amount
            self.sell_amount[-1] = bought * float(self.rowslist[index][2])
            self.sell_met_target[-1] = "1"

            """Use of Transaction Class"""
            date = str(self.rowslist[index])[2:12]
            time = str(self.rowslist[index])[12:18]
            print_object = transaction(self.path_to_transaction_file)
            print_object.print_transaction_items(date, time, self.line[0], "0", str(bought),
                                                 str(self.rowslist[index][2]),
                                                 str(sell_amount), "1")

            '''
            self.transactions_file.writerow(str(self.rowslist[index])[2:12] +
                                            str(self.rowslist[index])[12:18] +
                                            self.line[0] + "0" + str(bought) + str(self.rowslist[index][2]) +
                                            str(sell_amount) +  "1")
            '''
            return True
        return False

    def sell_stock_due_to_stop_loss(self, bought, close_price, index):
        per = (float(self.rowslist[index][2]) - close_price) / close_price
        if per <= self.stop_loss:
            sell_amount = bought * float(self.rowslist[index][2])
            self.total_sell = self.total_sell + sell_amount
            self.overall_sell = self.overall_sell + sell_amount
            self.total_sold += bought
            self.logger.info(
                "Stop Loss Sale: Stock " + self.line[0] + " sold " + str(bought) + " shares at " + self.rowslist[index][
                    2] + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[
                                                                                             13:18] + "\n")
            self.overall_c_stoploss = self.overall_c_stoploss + 1
            self.c_total_stoploss = self.c_total_stoploss + 1
            # the last element has already been initialised to  0.  modify it to the sold amount
            self.sell_amount[-1] = bought * float(self.rowslist[index][2])
            self.sell_stop_loss[-1] = "1"

            """Use of Transaction Class"""
            date = str(self.rowslist[index])[2:12]
            time = str(self.rowslist[index])[12:18]
            print_object = transaction(self.path_to_transaction_file)
            print_object.print_transaction_items(date, time, self.line[0], "0", str(bought),
                                                 str(self.rowslist[index][2]),
                                                 str(sell_amount), "2")

            '''
            self.transactions_file.writerow(str(self.rowslist[index])[2:12] +
                                            str(self.rowslist[index])[12:18] +
                                            self.line[0] + "0" + str(bought) + str(self.rowslist[index][2]) +
                                            str(sell_amount) + "1")
            '''
            return True
        return False

    def sell_stock_at_end_of_day(self, bought, close_price, index):
        self.total_sold += bought
        self.total_sell = self.total_sell + bought * float(self.rowslist[index][1])
        self.overall_sell = self.overall_sell + bought * float(self.rowslist[index][1])
        self.logger.info("Stock " + self.line[0] + " sold " + str(bought) + " shares at " + self.rowslist[index][
            1] + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[
                                                                                     13:18] + "\n")
        self.overall_c_sellEod = self.overall_c_sellEod + 1
        self.c_total_sellEOD = self.c_total_sellEOD + 1
        # the last element has already been initialised to  0.  modify it to the sold amount
        self.sell_amount[-1] = bought * float(self.rowslist[index][1])
        self.sell_EOD[-1] = "1"

        print_object = transaction(self.path_to_transaction_file)
        date = str(self.rowslist[index])[2:12]
        time = str(self.rowslist[index])[12:18]
        print_object.print_transaction_items(date, time, self.line[0], "0", str(bought), "0",
                                             str(self.rowslist[index][2]),
                                             str(self.sell_amount[-1]), "3")

    '''
        self.transactions_file.writerow(str(self.rowslist[index])[2:12] +
                                        str(self.rowslist[index])[12:18] +
                                        self.line[0] + "0" + str(bought) + str(self.rowslist[index][2]) +
                                        str(sell_amount) + "1")
    '''

    def DCH(self):
        # Function for inmplementing strategy-daily closing higher

        """Folders needed"""
        """This is just for reference, the name of the folder is not used as variable throughout the program"""
        strategy_folder = "Daily_closing_higher/"
        ndays = 3
        strategy_daily_closing_high.get_daily_closing_high(ndays, strategy_folder)

        # the list that contains the symbols for all the stocks that need to be downloaded
        # path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/modified_ind_nifty50list.csv"
        # path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/ind_niftyfmcglist.csv"
        path_to_stock_master_list = \
            self.obj.path_to_output_dir() + strategy_folder + "scanner_output.csv"
        # directory path to the historical data. Ensure that there is a / at the end
        path_to_historical_data = self.obj.path_to_historical_5_min_dir()

        path_to_index_file = self.obj.path_to_index_dir() + "NIFTY.csv"
        # path_to_index_file = "C:/Users/Rohit/Python_source_code/historical_indices_5_min_data/CNXFMCG.csv"

        path_to_output_directory = self.obj.path_to_output_dir() + strategy_folder

        self.path_to_transaction_file = path_to_output_directory + "transactions.csv"

        self.column_no_of_ticker = 0
        with open(path_to_stock_master_list, 'r') as f:
            self.lines = csv.reader(f)
            for self.line in self.lines:
                if "Symbol" not in self.line:
                    if '&' in self.line[self.column_no_of_ticker]:
                        ''''modification required: mmodify the code to include the _ depending on the file name
                        self.line[self.column_no_of_ticker] = self.line[self.column_no_of_ticker][
                                                              :self.line[self.column_no_of_ticker].index('&')] \
                                                              + "_26" + self.line[self.column_no_of_ticker][
                                                                        self.line[self.column_no_of_ticker].index(
                                                                            '&') + 1:]'''
                        self.line[self.column_no_of_ticker] = self.line[self.column_no_of_ticker][
                                                              :self.line[self.column_no_of_ticker].index('&')] \
                                                              + "%26" + self.line[self.column_no_of_ticker][
                                                                        self.line[self.column_no_of_ticker].index(
                                                                            '&') + 1:]

                    with open(path_to_historical_data + self.line[self.column_no_of_ticker] + ".csv", 'r') as g:
                        # re-initialise all the variables for the output columns as we have started reading a new stock
                        '''
                        self.recorded_date = []
                        self.day_open_price = []
                        self.rejected_price = []
                        self.buy_amount = []
                        self.sell_amount = []
                        '''
                        self.recorded_date = ["Date"]
                        self.day_open_price = ["Day Open"]
                        self.rejected_price = ["Rejected Price"]
                        self.rejected_volume = ["Rejected Volume"]
                        self.buy_amount = ["Purchase amount"]
                        self.sell_amount = ["Sell amount"]
                        self.index_in_same_direction = ["Index In Same Direction"]
                        self.sell_stop_loss = ["Sell Stop Loss"]
                        self.sell_EOD = ["Sell EOD"]
                        self.sell_met_target = ["Sell Met Target"]
                        self.buy_transaction = ["Buy"]

                        self.logger.info("Stock = " + self.line[self.column_no_of_ticker] + "\n")
                        print('\n', self.line[self.column_no_of_ticker])
                        rows = csv.reader(g)
                        self.rowslist = list(rows)
                        index = -1
                        open_price = 0.0
                        close_price = 0.0
                        index_open = 1
                        index_close = 1
                        self.total_cost = 0.0
                        self.total_sell = 0.0
                        self.c_total_wins = 0
                        self.c_total_sellEOD = 0
                        date = '0'
                        # scan for the date in the historical data that matches the date provided by the
                        # previous algorithm ( in this case the daily closing higher which
                        # selects the ticker symbol and the date for which the ticker symbol needs to be scanned
                        for row in self.rowslist:
                            if str(self.line[ndays + 1]) == str(row[0])[:10]:
                                index = self.rowslist.index(row)

                                # found the date for a particular stock from which we have to scan
                                # for trading opportunities. Reset all stock specific counters
                                self.total_cost = 0.0
                                self.total_sell = 0.0
                                self.c_total_wins = 0
                                self.c_total_sellEOD = 0
                                self.c_total_stoploss = 0
                                bought = 0
                                self.c_transactions_today = 0

                                # initialise output variables
                                self.new_output_row()

                                ndays_scanned = 0

                                break

                        # After getting the index, the closing of the previous day
                        i = 1
                        # move backwards one row at a time - select the first row which does not have any header
                        # there is implicit logic that the preceding non-header row will be of the previous day because
                        # the current row is the first occurrence of a new day since we are moving one candle at a time
                        # and so the first candle where we encounter a particular date is also the beginning of the day
                        # for that date
                        while 'Close' in self.rowslist[index - i]:
                            i = i + 1
                        prev_close_price = float(self.rowslist[index - i][1])

                        date = str(self.rowslist[index][0])[:10]
                        prev_day_date = str(self.rowslist[index - i][0])[:10]

                        # unexpected condition:  we expect the previous road to always have a different date (TODO:
                        # tighten the condition by testing that it should be before the current date)
                        if (prev_day_date == date):
                            self.logger.critical("Data is corrupted")

                        index_open = index
                        open_price = float(self.rowslist[index][4])
                        # print(open_price)
                        self.day_open_price[-1] = str(open_price)
                        do_not_buy = 0

                        c = 0
                        # initial value of index
                        # = index of the row with the first occurrence of the date from which we have to scan
                        while index < len(self.rowslist):
                            row = self.rowslist[index]

                            # do not read data which contains  headers such as "Close"
                            if 'Close' in row:
                                index += 1
                                continue

                            # Current price of the stock
                            current_price = float(row[1])

                            if row[0][:10] != date[:10]:
                                # encountered a new date;
                                date = row[0][:10]
                                do_not_buy = 1
                                ndays_scanned = ndays_scanned + 1
                                # stop scanning if we exceed the threshold of number of days to be scanned from the date
                                # recommended by the previous algorithm ( in this case the daily closing higher)
                                if ndays_scanned > self.max_ndays_scan:
                                    break

                            # if no stocks have been bought as yet...
                            if bought == 0 and do_not_buy == 0:
                                # ... and the current price is near the closing price of the previous day
                                if abs(prev_close_price - current_price) \
                                        < abs(self.deviation_from_prev_close * prev_close_price):
                                    # ... and the corresponding index is also increasing
                                    '''
                                    if is_index_in_same_direction.is_index_in_same_direction(path_to_index_file, 1,
                                                                                             date) \
                                    '''
                                    if True:
                                        # ... simulate the buying of stocks

                                        # 1. if there are more than one transactions, initialise a new row for output
                                        if (self.c_transactions_today > 0):
                                            self.new_output_row()
                                        # print("Transactions today: ", self.c_transactions_today)
                                        # ... & update the output
                                        self.index_in_same_direction[-1] = "1"
                                        self.recorded_date[-1] = date
                                        self.day_open_price[-1] = str(open_price)

                                        # 2. buy the stocks at the current price and  update the tracking counters
                                        bought = self.buy_stocks(current_price, index)
                                        purchase_price = current_price

                            if bought != 0:
                                if self.sell_stock_due_to_price_check(bought, purchase_price, index):
                                    bought = 0
                                    ndays_scanned = 0
                            if bought != 0:
                                if self.sell_stock_due_to_stop_loss(bought, purchase_price, index):
                                    bought = 0
                                    ndays_scanned = 0
                            '''        
                            print("ndays scanned = " + str(ndays_scanned) + "\n" + "max ndays = " + str(
                                self.max_ndays_scan) + "\n" + "bought: " + str(bought) + "\n" + str(self.rowslist[index]))
                            '''
                            if (ndays_scanned == self.max_ndays_scan) or (index == len(self.rowslist)):
                                if "15:30" in self.rowslist[index][0] and bought != 0:
                                    self.sell_stock_at_end_of_day(bought, purchase_price, index)
                                    bought = 0
                                    ndays_scanned = 0

                            index += 1

                        # this is unexpected condition. It may happen only if  there has been no trade at 15:15
                        if bought != 0:
                            self.logger.error("***Error: could not sell stock  = ***" + "\n")
                            self.logger.error("***ndays scanned = " + str(ndays_scanned) + "\n" + "max ndays = " + str(
                                self.max_ndays_scan) + "\n")
                            print("***Error: could not sell stock  = ***" + "\n")
                            print("***ndays scanned = " + str(ndays_scanned) + "\n" + "max ndays = " + str(
                                self.max_ndays_scan) + "\n")

                        self.logger.info(
                            "Total buy = " + str(self.total_cost) + " total sell = " + str(self.total_sell) +
                            " and total profit = " + str(self.total_sell - self.total_cost) + " for stock " +
                            self.line[self.column_no_of_ticker] + "\n")
                        self.logger.info("Total wins = " + str(self.c_total_wins) + " Total sell EOD = " +
                                         str(self.c_total_sellEOD) + " Stop Loss = " + str(
                            self.c_total_stoploss) + "\n")

                        rows = zip(self.recorded_date, self.day_open_price, self.buy_amount, self.sell_amount,
                                   self.buy_transaction, self.sell_met_target, self.sell_EOD, self.sell_stop_loss)

                        with open(path_to_output_directory + self.line[self.column_no_of_ticker] + ".csv", 'w',
                                  newline="") as f:
                            writer = csv.writer(f)
                            for row in rows:
                                writer.writerow(row)
                            f.close()
        self.logger.info(
            "Total purchases = " + str(self.total_purchased) + " total sold = " + str(self.total_sold) + "\n")
        self.logger.info(
            "Overall cost = " + str(self.overall_cost) + " Overall sell = " + str(self.overall_sell) + "\n")
        self.logger.info("Overall profit = " + str(self.overall_sell - self.overall_cost)
                         + " Overall Profit % = " + str(
            (self.overall_sell - self.overall_cost) / (self.overall_cost) * 100) + "\n")
        self.logger.info(
            "Overall buys = " + str(self.c_overall_buy_trans) + " Overall wins = " + str(self.overall_c_wins) +
            " Overall sell EOD = " + str(self.overall_c_sellEod) + " Overall stoploss = " + str(
                self.overall_c_stoploss) + "\n")


def main():
    deviation_from_prev_close = 0.02
    max_price_volatility = 100
    max_deviation_from_open = 100
    max_volume_volatility = 100
    max_capital_for_single_buy = 10000
    target_price = 0.01
    # the stoploss needs to be negative.
    stop_loss = -0.005
    max_ndays_scan = 3
    obj = config.config(r"../config.txt")
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=obj.path_to_output_dir() + "Daily_closing_higher/dch_log.Log", level=logging.DEBUG,
                        format=LOG_FORMAT, filemode='w')
    logger = logging.getLogger()
    logger.info(" Configuration for this run: " + "\n" + " deviation from previous close: " + str(
        deviation_from_prev_close) + "\n")
    logger.info(" target price:" + str(target_price) + " stoploss: " + str(stop_loss) + "\n")
    logger.info(" maximum capital for single purchase: " + str(max_capital_for_single_buy) + "\n")
    logger.info("Maximum days tto hold a position: " + str(max_ndays_scan) + "\n")
    obj = DCH(deviation_from_prev_close, max_price_volatility, max_deviation_from_open, max_volume_volatility,
              max_capital_for_single_buy,
              target_price, stop_loss, max_ndays_scan)
    logger.info(" maximum number of days to scan: " + str(max_ndays_scan) + "\n")
    obj.DCH()


main()
