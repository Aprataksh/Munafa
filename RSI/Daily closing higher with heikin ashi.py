import csv 
import sys 
import pandas as pd 
import logging
sys.path.insert(0, r"..\utilities") 
import is_index_in_same_direction
import scanner_daily_closing_high 
import config
import Buy_Sell 
sys.path.insert(1,r"..\Heikin-Ashi") 
import heikin_ashi

class DCH_HA(Buy_Sell.Buy_sell):
    obj = config.config(r"../config.txt")
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=obj.path_to_output_dir() + "Daily_closing_higher_with_heikin_ashi/dch_log.Log", level=logging.DEBUG,
                        format=LOG_FORMAT, filemode='w')
    logger = logging.getLogger()

    def __init__(self, dfpc, mpv, mdfo, mvv, mcfsb, tp, sl, mns, it, tsl, tsld, pos_flag, utsl):
        self.deviation_from_prev_close = dfpc
        self.max_price_volatility = mpv
        self.max_deviation_from_open = mdfo
        self.max_volume_volatility = mvv
        self.max_capital_for_single_buy = mcfsb
        self.target_price = tp
        self.stop_loss = sl
        self.initial_stoploss = self.stop_loss
        self.recorded_date = []
        self.day_open_price = []
        self.max_ndays_scan = mns
        tf = open(self.obj.path_to_output_dir() + "Daily_closing_higher_with_heikin_ashi/transactions.csv", 'w', newline="")
        self.transactions_file = csv.writer(tf)
        self.initial_target = it
        self.trailing_sl = tsl
        self.trailing_sl_diff = tsld
        self.position_flag=pos_flag
        self.use_tsl = utsl

    def initialise_output_headers_row(self):
        self.recorded_date = ["Date"]
        self.day_open_price = ["Day Open"]
        self.rejected_price = ["Rejected Price"]
        self.rejected_volume = ["Rejected Volume"]
        self.buy_amount = ["Purchase amount"]
        self.sell_amount = ["Sell amount"]
        self.sell_with_brokerage = ["Sell with brokerage"]
        self.index_in_same_direction = ["Index In Same Direction"]
        self.sell_stop_loss = ["Sell Stop Loss"]
        self.sell_EOD = ["Sell EOD"]
        self.sell_met_target = ["Sell Met Target"]
        self.buy_transaction = ["Buy"]

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
        self.sell_with_brokerage.append("0")

    def DCH_HA(self):
        # Function for inmplementing strategy-daily closing higher

        """This is just for reference, the name of the folder is not used as variable throughout the program"""
        strategy_folder = "Daily_closing_higher_with_heikin_ashi/"
        ndays = 2
        self.logger.info("number of days to scan for daily closing higher: " + str(ndays) + "\n\n")
        scanner_daily_closing_high.get_daily_closing_high(ndays, strategy_folder)
        #heikin_ashi.main(self.obj.path_to_historical_5_min_dir())
        # the list that contains the symbols for all the stocks that need to be
        # downloaded
        path_to_stock_master_list = \
            self.obj.path_to_output_dir() + strategy_folder + "scanner_output.csv"
        # directory path to the historical data.  Ensure that there is a / at
        # the end
        path_to_historical_data = self.obj.path_to_historical_5_min_dir()

        # path to the index file that contains the data for the corresponding
        # index
        path_to_index_file = self.obj.path_to_index_dir() + "NIFTY.csv"

        # path to the output directory where the log, the transactions etc are
        # printed
        path_to_output_directory = self.obj.path_to_output_dir() + strategy_folder

        self.path_to_transaction_file = path_to_output_directory + "transactions.csv"

        """Column Object and getting columns"""
        col_object = config.col_num("../config.txt")

        self.column_no_of_ticker = col_object.get_scanner_ticker_col()
        self.datetime_column = col_object.get_datetime_col()
        self.close_column = col_object.get_close_col()
        self.high_column = col_object.get_high_col()
        self.open_column = col_object.get_open_col()

        with open(path_to_stock_master_list, 'r') as f:
            self.lines = csv.reader(f)
            for self.line in self.lines:
                if "Symbol" not in self.line:
                    if '&' in self.line[self.column_no_of_ticker]:
                        ''''modification required: modify the code to include the _ depending on the file name
                        self.line[self.column_no_of_ticker] = self.line[self.column_no_of_ticker][
                                                              :self.line[self.column_no_of_ticker].index('&')] \
                                                              + "_26" + self.line[self.column_no_of_ticker][
                                                                        self.line[self.column_no_of_ticker].index(
                                                                            '&') + 1:]'''
                        self.line[self.column_no_of_ticker] = self.line[self.column_no_of_ticker][:self.line[self.column_no_of_ticker].index('&')] \
                                                              + "%26" + self.line[self.column_no_of_ticker][self.line[self.column_no_of_ticker].index('&') + 1:]

                    with open(path_to_historical_data + self.line[self.column_no_of_ticker] + ".csv", 'r') as g:
                        # initialised the headers for output
                        self.initialise_output_headers_row()
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
                        df_ha = pd.read_csv(self.obj.path_to_output_dir() + "Heikin-Ashi/" + self.line[self.column_no_of_ticker] + ".csv")
                        ha_close = df_ha['Close']
                        ha_open = df_ha['Open']
                        # scan for the date in the historical data that matches
                        # the date provided by the
                        # previous algorithm ( in this case the daily closing
                        # higher which
                        # selects the ticker symbol and the date for which the
                        # ticker symbol needs to be scanned
                        for row in self.rowslist:
                            # if we are looking for 2 days that the stock must
                            # close higher, then compare
                            # the date in the 2 + 1 column to the date in the
                            # row to see if they match
                            # TODO :
                            # https://github.com/Aprataksh/Munafa/issues/8
                            if str(self.line[ndays + 1]) == str(row[self.datetime_column])[:10]:
                                index = self.rowslist.index(row)

                                # found the date for a particular stock from
                                # which we have to scan
                                # for trading opportunities.  Reset all stock
                                # specific counters
                                self.total_cost = 0.0
                                self.total_sell = 0.0
                                self.c_total_wins = 0
                                self.c_total_sellEOD = 0
                                self.c_total_stoploss = 0
                                bought = 0
                                self.c_transactions_today = 0
                                self.stop_loss = self.initial_stoploss

                                # initialise output variables
                                self.new_output_row()

                                ndays_scanned = 0
                                # once the date match,  break out of the loop to start scanning from the row after
                                # the the dates had matched to look for potential trades
                                break

                        # After getting the index, the closing of the previous
                        # day
                        i = 1
                        # move backwards one row at a time - select the first
                        # row which does not have any header
                        # there is implicit logic that the preceding non-header
                        # row will be of the previous day because
                        # the current row is the first occurrence of a new day
                        # since we are moving one candle at a time
                        # and so the first candle where we encounter a
                        # particular date is also the beginning of the day
                        # for that date
                        while 'Close' in self.rowslist[index - i]:
                            i = i + 1
                        prev_close_price = float(self.rowslist[index - i][self.close_column])

                        date = str(self.rowslist[index][self.datetime_column])[:10]
                        prev_day_date = str(self.rowslist[index - i][self.datetime_column])[:10]

                        # unexpected condition: we expect the previous road to
                        # always have a different date (TODO:
                        # tighten the condition by testing that it should be
                        # before the current date)
                        if (prev_day_date == date):
                            self.logger.critical("Data is corrupted OR the data files to not have the same duration")
                            self.logger.critical("Moving to the next stock...")
                            continue

                        index_open = index
                        open_price = float(self.rowslist[index][self.open_column])
                        # print(open_price)
                        self.day_open_price[-1] = str(open_price)
                        do_not_buy = 0
                        purchase_date = date[:10]
                        c = 0
                        # initial value of index
                        # = index of the row with the first occurrence of the
                        # date from which we have to scan
                        while index < len(self.rowslist):
                            row = self.rowslist[index]

                            # do not read data which contains headers such as
                            # "Close"
                            if 'Close' in row:
                                index += 1
                                continue

                            # Current price of the stock
                            current_price = float(row[self.close_column])

                            if row[0][:10] != date[:10]:
                                # encountered a new date;
                                date = row[0][:10]
                                do_not_buy = 1
                                ndays_scanned = ndays_scanned + 1
                                # stop scanning if we exceed the threshold of
                                # number of days to be scanned from the date
                                # recommended by the previous algorithm ( in
                                # this case the daily closing higher)
                                if ndays_scanned > self.max_ndays_scan:
                                    break

                            # if no stocks have been bought as yet...
                            if bought == 0 and do_not_buy == 0:
                                # ...  and the current price is near the
                                # closing price of the previous day
                                # previous_col_correct and current_col_correct are counters to check if the color is red/green
                                # acc. to the value of position_flag

                                # we subtract one from the index  to find the current index in the RSI file because
                                # the variable index refers to the historical data file which contains one additional header
                                # row
                                current_index = index - 1
                                previous_index = index - 2
                                if ha_close[current_index] > ha_open[current_index]:
                                    if self.position_flag == 1:
                                        current_col_correct = True
                                    else:
                                        current_col_correct = False
                                else:
                                    if self.position_flag == 1:
                                        current_col_correct = False
                                    else:
                                        current_col_correct = True
                                if ha_close[previous_index] > ha_open[previous_index]:
                                    if self.position_flag == 1:
                                        previous_col_correct = True
                                    else:
                                        previous_col_correct = False
                                else:
                                    if self.position_flag == 1:
                                        previous_col_correct = False
                                    else:
                                        previous_col_correct = True
                                if current_col_correct and previous_col_correct:
                                    # ...  and the corresponding index is also
                                    # increasing
                                    if is_index_in_same_direction.is_index_in_same_direction(path_to_index_file, self.position_flag,
                                                                                             str(self.rowslist[index][0])):
                                    # if  True:
                                        # ...  simulate the buying of stocks

                                        # 1.  if there are more than one
                                        # transactions, initialise a new row
                                        # for output
                                        if (self.c_transactions_today > 0):
                                            self.new_output_row()
                                        # print("Transactions today: ",
                                        # self.c_transactions_today)
                                        # ...  & update the output
                                        self.index_in_same_direction[-1] = "1"
                                        self.recorded_date[-1] = date
                                        self.day_open_price[-1] = str(open_price)

                                        # 2.  buy the stocks at the current
                                        # price and update the tracking
                                        # counters
                                        bought = self.buy_stocks(current_price, index)
                                        purchase_price = current_price

                            if bought != 0:
                                if self.sell_stock_due_to_price_check(bought, purchase_price, purchase_date, index):
                                    bought = 0
                                    ndays_scanned = 0

                            if bought != 0:

                                if self.use_tsl == 1:
                                    if (self.position_flag == 1 and
                                        float(self.rowslist[index][self.close_column]) > purchase_price) or\
                                            (self.position_flag == -1 and
                                             float(self.rowslist[index][self.close_column]) < purchase_price):
                                        self.logger.info("index " + str(index) + " " + str(row) + "\n")
                                        if self.initial_target_met(purchase_price, index) == True:
                                            self.trailing_stoploss(self.initial_stoploss, purchase_price, index)
                                            self.logger.info("Stop-loss Changed = " + str(self.stop_loss) + " from " + str(self.initial_stoploss))
                                if self.sell_stock_due_to_stop_loss(bought, purchase_price, purchase_date, index):
                                    bought = 0
                                    ndays_scanned = 0
                            '''        
                            print("ndays scanned = " + str(ndays_scanned) + "\n" + "max ndays = " + str(
                                self.max_ndays_scan) + "\n" + "bought: " + str(bought) + "\n" + str(self.rowslist[index]))
                            
                            self.logger.error("***dump  = ***" + str(index)+ " " +
                                              str(len(self.rowslist)) + " " +
                                              str(config.config.trading_closing_time)+"\n")
                            '''
                            if (ndays_scanned == self.max_ndays_scan) and bought != 0:
                                if config.config.trading_closing_time in self.rowslist[index][self.datetime_column]:
                                    self.sell_stock_at_end_of_day(bought, purchase_price, purchase_date, index)
                                    bought = 0
                                    ndays_scanned = 0

                            if (index == len(self.rowslist) - 1) and bought != 0:
                                self.logger.info("End of day sale at time: " + str(self.rowslist[index][self.datetime_column]) + "\n")
                                self.sell_stock_at_end_of_day(bought, purchase_price, purchase_date, index)
                                bought = 0
                                ndays_scanned = 0

                            index += 1

                        # this is unexpected condition.  It may happen only if
                        # there has been no trade at 15:15
                        if bought != 0:
                            self.logger.error("***Error: could not sell stock  = ***" + "\n")
                            self.logger.error("***ndays scanned = " + str(ndays_scanned) + "\n" + "max ndays = " + str(self.max_ndays_scan) + "\n")
                            print("***Error: could not sell stock  = ***" + "\n")
                            print("***ndays scanned = " + str(ndays_scanned) + "\n" + "max ndays = " + str(self.max_ndays_scan) + "\n")

                        self.logger.info("Total buy = " + str(self.total_cost) + " total sell = " + str(self.total_sell) + " and total profit = " 
                        	+ str(self.total_sell - self.total_cost) + " for stock " + self.line[self.column_no_of_ticker] + "\n")
                        self.logger.info("Total wins = " + str(self.c_total_wins) + " Total sell EOD = " + str(self.c_total_sellEOD) + " Stop Loss = " 
                        	+ str(self.c_total_stoploss) + "\n")


                        rows = zip(self.recorded_date, self.day_open_price, self.buy_amount, self.sell_amount,
                                   self.buy_transaction, self.sell_met_target, self.sell_EOD, self.sell_stop_loss)

                        with open(path_to_output_directory + self.line[self.column_no_of_ticker] + ".csv", 'w',
                                  newline="") as f:
                            writer = csv.writer(f)
                            for row in rows:
                                writer.writerow(row)
                            f.close()

        overall_profit = (self.overall_sell - self.overall_cost) / (self.overall_cost) * 100
        self.logger.info("Total purchases = " + str(self.total_purchased) + " total sold = " + str(self.total_sold) + "\n")
        self.logger.info("Overall cost = " + str(self.overall_cost) + " Overall sell = " + str(self.overall_sell) + " Overall sell with brokerage = " 
        	+ str(self.overall_sell_with_brokerage) + "\n")
        self.logger.info("Overall profit = " + str(self.overall_sell - self.overall_cost) + " Overall Profit % = " + str(overall_profit) + "\n")
        self.logger.info("Overall buys = " + str(self.c_overall_buy_trans) + " Overall wins = " + str(self.overall_c_wins) + " Overall sell EOD = " 
        	+ str(self.overall_c_sellEod) + " Overall stoploss = " + str(self.overall_c_stoploss) + "\n")
        percentage_wins = (self.overall_c_wins / self.c_overall_buy_trans) * 100
        profit_after_brokerage = self.overall_sell_with_brokerage - self.overall_cost
        percentage_intraday = \
            (self.overall_c_intraday / (self.overall_c_wins + self.overall_c_stoploss + self.overall_c_sellEod)) * 100
        percentage_loss_intraday = (self.c_intraday_losses / self.overall_c_intraday) * 100
        self.logger.info("Percentage wins: " + str(percentage_wins) + "  profit after brokerage: " + str(
            profit_after_brokerage) + "\n")
        self.logger.info(" Intraday sales "
                         + str(self.overall_c_intraday) + " Intraday percentage " + str(percentage_intraday) + "\n")
        self.logger.info(" Intraday losses " + str(self.c_intraday_losses) + " Intraday loss percentage "
                         + str(percentage_loss_intraday) + " overall trailing stoploss:" + str(
            self.overall_c_trailing) + "\n")

def main():
    deviation_from_prev_close = 0.002
    max_price_volatility = 100
    max_deviation_from_open = 100
    max_volume_volatility = 100
    max_capital_for_single_buy = 10000
    target_price = 0.015
    # the stoploss needs to be negative.
    stop_loss = -0.008
    max_ndays_scan = 3
    initial_target = 0.03
    trailing_stop_loss = 0.005
    tsl_difference = initial_target - trailing_stop_loss
    # should be used trailing stoploss or not; I signed it the value of 1  to use trailing stop loss.if it is 0,
    # the value of initial target, trailing stoploss and tsl difference are ignored
    use_tsl = 0
    # for a short position, assign the value of -1. For a long position, assign the value of 1
    position_type = 1
    obj = config.config(r"../config.txt")
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=obj.path_to_output_dir() + "Daily_closing_higher_with_heikin_ashi/dch_log.Log", level=logging.DEBUG,
                        format=LOG_FORMAT, filemode='w')
    logger = logging.getLogger()
    logger.info(" Configuration for this run: " + "\n" + " deviation from previous close: " + str(deviation_from_prev_close) + "\n")
    logger.info(" target price:" + str(target_price) + " stoploss: " + str(stop_loss) + "\n")
    logger.info(" maximum capital for single purchase: " + str(max_capital_for_single_buy) + "\n")
    logger.info("Maximum days to hold a position: " + str(max_ndays_scan) + "\n")
    obj = DCH_HA(deviation_from_prev_close, max_price_volatility, max_deviation_from_open, max_volume_volatility,
              max_capital_for_single_buy,
              target_price, stop_loss, max_ndays_scan, initial_target, trailing_stop_loss, tsl_difference, position_type,
              use_tsl)
    logger.info(" position type(Long or Short): " + str(position_type) + " using trailing stoploss: " +
                " initial target for trailing stoploss: " + str(initial_target)  + "\n" )
    logger.info(" trailing stoploss: " + str(trailing_stop_loss) + "trailing stoploss difference: " + str(tsl_difference) + "\n")
    obj.DCH_HA()


main()
