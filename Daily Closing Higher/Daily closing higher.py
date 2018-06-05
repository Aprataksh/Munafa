import csv
import sys
import pandas as pd
sys.path.insert(0, r"..\utilities")
import is_index_in_same_direction
import strategy_daily_closing_high


class OHL():
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
    def __init__(self, dfpc, mpv, mdfo, mvv, mcfsb, tp, sl):
        self.deviation_from_prev_close = dfpc
        self.max_price_volatility = mpv
        self.max_deviation_from_open = mdfo
        self.max_volume_volatility = mvv
        self.max_capital_for_single_buy = mcfsb
        self.target_price = tp
        self.stop_loss = sl
        self.recorded_date = []
        self.day_open_price = []

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
            self.total_cost = self.total_cost + (bought * purchase_cost)
            self.total_purchased += bought
            self.overall_cost = self.overall_cost + (bought * purchase_cost)
            self.c_overall_buy_trans = self.c_overall_buy_trans + 1
            self.c_transactions_today  = self.c_transactions_today  + 1
            self.buy_amount[-1] = str(bought * purchase_cost)
            print("Stock " + self.line[0] + " bought " + str(bought) + " shares at " + str(
                purchase_cost) + " price at date " + str(self.rowslist[index_close])[2:12] + " at time " + str(
                self.rowslist[index_close])[12:18] + "\n")
        else:
            # this may happen if the price of one stock is more than the  maximum capital
            print("Could not buy stock " + self.line[0] + " on date " + str(self.rowslist[index_close])[
                                                                        2:12] + " due to insufficient daily stock fund\n")
        return bought

    def sell_stock_due_to_price_check(self, bought, close_price, index):
        per = (float(self.rowslist[index][2]) - close_price) / close_price
        if per >= self.target_price:
            self.total_sell = self.total_sell + bought * float(self.rowslist[index][2])
            self.overall_sell = self.overall_sell + bought * float(self.rowslist[index][2])
            self.total_sold += bought
            print("Stock " + self.line[0] + " sold " + str(bought) + " shares at " + self.rowslist[index][
                2] + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[
                                                                                         13:18] + "\n")
            self.overall_c_wins = self.overall_c_wins + 1
            self.c_total_wins = self.c_total_wins + 1
            # the last element has already been initialised to  0.  modify it to the sold amount
            self.sell_amount[-1] = bought * float(self.rowslist[index][2])
            self.sell_met_target[-1] = "1"
            return True
        return False

    def sell_stock_due_to_stop_loss(self, bought, close_price, index):
        per = (float(self.rowslist[index][2]) - close_price) / close_price
        if per <= self.stop_loss:
            self.total_sell = self.total_sell + bought * float(self.rowslist[index][2])
            self.overall_sell = self.overall_sell + bought * float(self.rowslist[index][2])
            self.total_sold += bought
            print(
                "Stop Loss Sale: Stock " + self.line[0] + " sold " + str(bought) + " shares at " + self.rowslist[index][
                    2] + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[
                                                                                             13:18] + "\n")
            self.overall_c_stoploss = self.overall_c_stoploss + 1
            self.c_total_stoploss = self.c_total_stoploss + 1
            # the last element has already been initialised to  0.  modify it to the sold amount
            self.sell_amount[-1] = bought * float(self.rowslist[index][2])
            self.sell_stop_loss[-1] = "1"
            return True
        return False

    def sell_stock_at_end_of_day(self, bought, close_price, index):
        self.total_sold += bought
        self.total_sell = self.total_sell + bought * float(self.rowslist[index][1])
        self.overall_sell = self.overall_sell + bought * float(self.rowslist[index][1])
        print("Stock " + self.line[0] + " sold " + str(bought) + " shares at " + self.rowslist[index][
            1] + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[
                                                                                     13:18] + "\n")
        self.overall_c_sellEod = self.overall_c_sellEod + 1
        self.c_total_sellEOD = self.c_total_sellEOD + 1
        # the last element has already been initialised to  0.  modify it to the sold amount
        self.sell_amount[-1] = bought * float(self.rowslist[index][1])
        self.sell_EOD[-1] = "1"

    def OHL(self):
        # Function for inmplementing strategy-daily closing higher
        ndays = 3
        strategy_daily_closing_high.get_daily_closing_high(ndays)

        # the list that contains the symbols for all the stocks that need to be downloaded
        # path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/modified_ind_nifty50list.csv"
        # path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/ind_niftyfmcglist.csv"
        path_to_stock_master_list = \
            "C:/Users/Rohit/Python_source_code/output/daily_closing_higher/daily_closing_higher_output.csv"
        # directory path to the historical data. Ensure that there is a / at the end
        path_to_historical_data = "C:/Users/Rohit/Python_source_code/historical_stock_5_min_data/"

        path_to_index_file = "C:/Users/Rohit/Python_source_code/historical_indices_5_min_data/NIFTY.csv"
        # path_to_index_file = "C:/Users/Rohit/Python_source_code/historical_indices_5_min_data/CNXFMCG.csv"

        path_to_output_directory = "C:/Users/Rohit/Python_source_code/output/daily_closing_higher/"
        self.column_no_of_ticker = 0
        with open(path_to_stock_master_list, 'r') as f:
            self.lines = csv.reader(f)
            for self.line in self.lines:
                if "Symbol" not in self.line:
                    if '&' in self.line[self.column_no_of_ticker]:
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
                        print('\n', self.line[self.column_no_of_ticker])
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

                                break

                        # After getting the index, the closing of the previous day
                        i = 1
                        # move backwards one row at a time - select the first row which does not have any header
                        # there is implicit logic that the preceding non-header row will be of the previous day because
                        # the current row is the first occurrence of a new day since we are moving one candle at a time
                        # and so the first candle where we encounter a particular date is also the beginning of the day
                        # for that date
                        while 'Close'  in self.rowslist[index - i]:
                            i = i + 1
                        prev_close_price = float(self.rowslist[index - i][1])

                        date = str(self.rowslist[index][0])[:10]
                        prev_day_date = str(self.rowslist[index - i][0])[:10]

                        # unexpected condition:  we expect the previous road to always have a different date (TODO:
                        # tighten the condition by testing that it should be before the current date)
                        if (prev_day_date == date):
                            print("***Error: Found the date of the what we think is previous day to be"
                                  " equal to the current date\n***")

                        index_open = index
                        open_price = float(self.rowslist[index][4])
                        # print(open_price)
                        self.day_open_price[-1] = str(open_price)

                        c = 0
                        # initial value of index
                        # = index of the row with the first occurrence of the date from which we have to scan
                        while index < len(self.rowslist):
                            row = self.rowslist[index]
                            if 'Close' in row:
                                index += 1
                                continue
                            #Current price of the stock
                            current_price = float(row[1])

                            # do not read data which contains  headers such as "Close"
                            if 'Close' in row:
                                index += 1
                                continue

                            if row[0][8:10] != date[8:10]:
                                # encountered a new date; stop scanning because they look at the dates
                                # recommended by the previous algorithm ( in this case the daily closing higher)
                                break


                            # Condition for the deviation of price from close price of previous day
                            if bought == 0:
                                if abs(prev_close_price - current_price) \
                                        < abs(self.deviation_from_prev_close * prev_close_price):
                                    # if there are more than one transactions, initialising a new draw for output
                                    if (self.c_transactions_today > 0):
                                        self.new_output_row()
                                    #print("Transactions today: ", self.c_transactions_today)
                                    self.recorded_date[-1] = date
                                    self.day_open_price[-1] = str(open_price)
                                    bought = self.buy_stocks(current_price, index)
                                    purchase_price = current_price

                            if bought != 0:
                                if self.sell_stock_due_to_price_check(bought, purchase_price, index):
                                    bought = 0
                            if bought != 0:
                                if self.sell_stock_due_to_stop_loss(bought, purchase_price, index):
                                    bought = 0
                            if "15:30" in self.rowslist[index][0] and bought != 0:
                                self.sell_stock_at_end_of_day(bought, purchase_price, index)
                                bought = 0

                            index += 1

                        # this is unexpected condition. It may happen only if  there has been no trade at 15:15
                        if bought != 0:
                            print("***Error: could not sell stock\n***")
                        print("Total buy = " + str(self.total_cost) + " total sell = " + str(self.total_sell) +
                              " and total profit = " + str(self.total_sell - self.total_cost) + " for stock " +
                              self.line[self.column_no_of_ticker] + "\n")
                        print("Total wins = " + str(self.c_total_wins) + " Total sell EOD = " +
                              str(self.c_total_sellEOD) + " Stop Loss = " + str(self.c_total_stoploss))

                        rows = zip(self.recorded_date, self.day_open_price, self.buy_amount, self.sell_amount,
                                   self.buy_transaction, self.sell_met_target, self.sell_EOD, self.sell_stop_loss)

                        with open(path_to_output_directory + self.line[self.column_no_of_ticker] + ".csv", 'w',
                                  newline="") as f:
                            writer = csv.writer(f)
                            for row in rows:
                                writer.writerow(row)
                            f.close()

        print("Total purchases = " + str(self.total_purchased) + " total sold = " + str(self.total_sold) + "\n")
        print("Overall cost = " + str(self.overall_cost) + " Overall sell = " + str(self.overall_sell) + "\n")
        print("Overall profit = " + str(self.overall_sell - self.overall_cost)
              + " Overall Profit % = " + str((self.overall_sell - self.overall_cost) / (self.overall_cost) * 100))
        print("Overall buys = " + str(self.c_overall_buy_trans) + " Overall wins = " + str(self.overall_c_wins) +
              " Overall sell EOD = " + str(self.overall_c_sellEod) + " Overall stoploss = " + str(
            self.overall_c_stoploss))



def main():
    deviation_from_prev_close = .02
    max_price_volatility = 100
    max_deviation_from_open = 100
    max_volume_volatility = 100
    max_capital_for_single_buy = 10000
    target_price = 0.008
    # the stoploss needs to be negative.
    stop_loss = -0.02

    print(" Configuration for this run: " + "\n" + " deviation from previous close: " + str(deviation_from_prev_close) + "\n")
    print(" target price:" + str(target_price) + " stoploss: " + str(stop_loss) + "\n")
    print(" maximum capital for single purchase: " + str(max_capital_for_single_buy) + "\n")

    obj = OHL(deviation_from_prev_close, max_price_volatility, max_deviation_from_open, max_volume_volatility, max_capital_for_single_buy,
              target_price, stop_loss)
    obj.OHL()


main()
