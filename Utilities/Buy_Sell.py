import sys
from datetime import datetime,timedelta
sys.path.insert(0, r"..\utilities")
import config
from config import brokerage
from transaction import transaction

class Buy_sell():

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
    datetime_column = 0
    close_column = 0
    high_column = 0
    open_column = 0
    overall_sell_with_brokerage = 0.0
    overall_c_intraday = 0
    overall_c_trailing = 0
    c_intraday_losses = 0
    folder_name = ""

    def buy_stocks(self, purchase_cost, index_close):
        config_obj = config.config(r"../config.txt")
        purchase_cutoff_time = config_obj.purchase_cutoff_time
        checkdate = self.rowslist[index_close][self.datetime_column][2:11] + purchase_cutoff_time[:4] + ":00"
        if 'pm' in purchase_cutoff_time or 'Pm' in purchase_cutoff_time or 'PM' in purchase_cutoff_time or 'pM' in purchase_cutoff_time:
            checkdate = datetime.strptime(checkdate, "%y-%m-%d %H:%M:%S") + timedelta(hours = 12)
        else:
            checkdate = datetime.strptime(checkdate, "%y-%m-%d %H:%M:%S")
        curr_date = datetime.strptime(self.rowslist[index_close][self.datetime_column][2:18], "%y-%m-%d %H:%M:%S")
        if curr_date < checkdate:
            bought = int(self.max_capital_for_single_buy / purchase_cost)
            if bought != 0:
                actual_cost = (bought * purchase_cost)
                self.total_cost = self.total_cost + actual_cost
                self.total_purchased += bought
                self.overall_cost = self.overall_cost + actual_cost
                self.c_overall_buy_trans = self.c_overall_buy_trans + 1
                self.c_transactions_today = self.c_transactions_today + 1
                self.buy_amount[-1] = str(actual_cost)
                self.logger.info("Stock " + self.line[self.column_no_of_ticker] + " bought " + str(bought) + " shares at " + str(purchase_cost) +
            	    " price at date " + str(self.rowslist[index_close])[2:12] + " at time " + str(self.rowslist[index_close])[12:18] + "\n")

                """Use of Transaction Class"""
                date = str(self.rowslist[index_close])[2:12]
                time = str(self.rowslist[index_close])[12:18]
                print_object = transaction(self.path_to_transaction_file)
                print_object.print_transaction_items(date, time, self.line[self.column_no_of_ticker], "1",
                                                     str(bought), str(purchase_cost), str(actual_cost), "0")

                '''
                self.transactions_file.writerow(str(self.rowslist[index_close])[2:12] +  str(self.rowslist[index_close])[12:18] +
                                                self.line[0] +  "1" +  str(bought) + str(purchase_cost) + str(0.0-actual_cost) +
                                                "0")
                '''
            else:
                # this may happen if the price of one stock is more than the
                # maximum capital
                self.logger.error("Could not buy stock " + self.line[0] + " on date " + str(self.rowslist[index_close])[2:12] +
            	    " due to insufficient daily stock fund\n")
            return bought
        else:
            self.logger.error(
                "Could not buy stock " + self.line[0] + " on date " + str(self.rowslist[index_close])[2:12] +
                " due to cut-off time for purchase\n")
            return 0

    def sell_stock_due_to_price_check(self, bought, purchase_price, purchase_date, index):
        current_close_price = float(self.rowslist[index][self.close_column])
        per = self.position_flag * ((current_close_price - purchase_price) / purchase_price)
        if per >= self.target_price:
            sell_amount = bought * current_close_price
            self.total_sell = self.total_sell + sell_amount
            self.overall_sell = self.overall_sell + sell_amount
            self.total_sold += bought
            sell_with_brokerage = 0.0
            brokerage_object = brokerage()
            if (purchase_date != self.rowslist[index][self.datetime_column][:10]):
                brokerage_fee = brokerage_object.calculate_delivery_brokerage(sell_amount)
                sell_with_brokerage = sell_amount - (self.position_flag * brokerage_fee)
                self.logger.info("Delivery Sale: " + "Sell amount: " + str(sell_amount) + " sell with brokerage: " + str(sell_with_brokerage) 
                	+ " Brokerage fee: " + str(brokerage_fee))
            else:
                brokerage_fee = brokerage_object.calculate_intraday_brokerage(sell_amount)
                sell_with_brokerage = sell_amount - brokerage_fee
                self.logger.info("Intraday Sale: " + "Sell amount: " + str(sell_amount) + " sell with brokerage: " + str(sell_with_brokerage) 
                	+ " Brokerage fee: " + str(brokerage_fee))
                self.overall_c_intraday = self.overall_c_intraday + 1

            self.overall_sell_with_brokerage = self.overall_sell_with_brokerage + sell_with_brokerage

            self.logger.info("Stock " + self.line[self.column_no_of_ticker] + " sold " + str(bought) + " shares at " + str(current_close_price) 
            	+ " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[13:18] + "\n")
            self.overall_c_wins = self.overall_c_wins + 1
            self.c_total_wins = self.c_total_wins + 1
            # the last element has already been initialised to 0.  modify it to
            # the sold amount
            self.sell_with_brokerage[-1] = sell_with_brokerage
            self.sell_amount[-1] = sell_amount
            self.sell_met_target[-1] = "1"

            """Use of Transaction Class"""
            date = str(self.rowslist[index])[2:12]
            time = str(self.rowslist[index])[12:18]
            print_object = transaction(self.path_to_transaction_file)
            print_object.print_transaction_items(date, time, self.line[self.column_no_of_ticker], "0", str(bought),
                                                 str(current_close_price),
                                                 str(sell_amount), "1")

            '''
            self.transactions_file.writerow(str(self.rowslist[index])[2:12] +
                                            str(self.rowslist[index])[12:18] +
                                            self.line[0] + "0" + str(bought) + str(self.rowslist[index][2]) +
                                            str(sell_amount) +  "1")
            '''
            return True
        return False

    def initial_target_met(self, purchase_price, index):
        current_close_price = float(self.rowslist[index][self.close_column])
        per = self.position_flag * ((float(self.rowslist[index][self.close_column]) - purchase_price) / purchase_price)
        if per > self.initial_target:
            self.stop_loss = self.trailing_sl
            self.logger.info("initial target met: Stock " + self.line[self.column_no_of_ticker] +
                             " Current price " + str(current_close_price) + " price at date " +
                             str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[13:18] + "\n")
            return True
        else:
            return False

    def trailing_stoploss(self, initial_stoploss, purchase_price, index):
        per = self.position_flag * ((float(self.rowslist[index][self.close_column]) - purchase_price) / purchase_price)
        if (per - self.trailing_sl_diff) > self.stop_loss:
            self.stop_loss = (per - self.trailing_sl_diff)

    def sell_stock_due_to_stop_loss(self, bought, purchase_price, purchase_date, index):
        current_close_price = float(self.rowslist[index][self.close_column])
        per = self.position_flag * ((current_close_price - purchase_price) / purchase_price)
        if per <= self.stop_loss:
            self.logger.info("SOLD at " + str(current_close_price) + " BOUGHT At = " + str(purchase_price) + " CURRENT STOPLOSS = " 
            	+ str(self.stop_loss) + " PER_CHANGE = " + str(per))

            if self.stop_loss > self.initial_stoploss:
                self.overall_c_trailing = self.overall_c_trailing + 1
                self.logger.info("TRAILING STOP LOSS SALE:")

            sell_amount = bought * current_close_price
            self.total_sell = self.total_sell + sell_amount
            self.overall_sell = self.overall_sell + sell_amount
            self.total_sold += bought
            sell_with_brokerage = 0.0
            brokerage_object = brokerage()
            if (purchase_date != self.rowslist[index][self.datetime_column][:10]):
                brokerage_fee = brokerage_object.calculate_delivery_brokerage(sell_amount)
                sell_with_brokerage = sell_amount - (self.position_flag * brokerage_fee)
                self.logger.info("Delivery Sale: " + "Sell amount: " + str(sell_amount) + " sell with brokerage: " + str(sell_with_brokerage) 
                	+ " Brokerage fee: " + str(brokerage_fee))
            else:
                brokerage_fee = brokerage_object.calculate_intraday_brokerage(sell_amount)
                sell_with_brokerage = sell_amount - (self.position_flag * brokerage_fee)
                self.logger.info("Intraday Sale: " + "Sell amount: " + str(sell_amount) + " sell with brokerage: " + str(sell_with_brokerage) 
                	+ " Brokerage fee: " + str(brokerage_fee))
                self.overall_c_intraday = self.overall_c_intraday + 1
                self.c_intraday_losses = self.c_intraday_losses + 1
                
            self.overall_sell_with_brokerage = self.overall_sell_with_brokerage + sell_with_brokerage

            self.logger.info("Stop Loss Sale: Stock " + self.line[self.column_no_of_ticker] + " sold " + str(bought) + " shares at " 
            	+ str(current_close_price) + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[13:18] + "\n")
            self.overall_c_stoploss = self.overall_c_stoploss + 1
            self.c_total_stoploss = self.c_total_stoploss + 1
            # the last element has already been initialised to 0.  modify it to
            # the sold amount
            self.sell_amount[-1] = sell_amount
            self.sell_stop_loss[-1] = "1"

            """Use of Transaction Class"""
            date = str(self.rowslist[index])[2:12]
            time = str(self.rowslist[index])[12:18]
            print_object = transaction(self.path_to_transaction_file)
            print_object.print_transaction_items(date, time, self.line[self.column_no_of_ticker], "0", str(bought),
                                                 str(current_close_price), str(sell_amount), "2")

            '''
            self.transactions_file.writerow(str(self.rowslist[index])[2:12] +
                                            str(self.rowslist[index])[12:18] +
                                            self.line[0] + "0" + str(bought) + str(self.rowslist[index][2]) +
                                            str(sell_amount) + "1")
            '''
            return True
        return False

    def sell_stock_at_end_of_day(self, bought, purchase_price, purchase_date,  index):
        current_close_price = float(self.rowslist[index][self.close_column])
        sell_amount = bought * current_close_price
        self.total_sold += bought
        self.total_sell = self.total_sell + sell_amount
        self.overall_sell = self.overall_sell + sell_amount
        sell_with_brokerage = 0.0
        brokerage_object = brokerage()
        if (purchase_date != self.rowslist[index][self.datetime_column][:10]):
            brokerage_fee = brokerage_object.calculate_delivery_brokerage(sell_amount)
            sell_with_brokerage = sell_amount - (self.position_flag * brokerage_fee)
            self.logger.info("Delivery Sale: " + "Sell amount: " + str(sell_amount) + " sell with brokerage: " + str(sell_with_brokerage) 
            	+ " Brokerage fee: " + str(brokerage_fee))
        else:
            brokerage_fee = brokerage_object.calculate_intraday_brokerage(sell_amount)
            sell_with_brokerage = sell_amount - brokerage_fee
            self.logger.info("Intraday Sale: " + "Sell amount: " + str(sell_amount) + " sell with brokerage: " + str(sell_with_brokerage) 
            	+ " Brokerage fee: " + str(brokerage_fee))
            self.overall_c_intraday = self.overall_c_intraday + 1
            if sell_with_brokerage < bought * purchase_price:
                self.c_intraday_losses = self.c_intraday_losses + 1

        self.overall_sell_with_brokerage = self.overall_sell_with_brokerage + sell_with_brokerage

        self.logger.info("Stock " + self.line[self.column_no_of_ticker] + " sold " + str(bought) + " shares at " + str(current_close_price) 
        	+ " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[13:18] + "\n")
        self.overall_c_sellEod = self.overall_c_sellEod + 1
        self.c_total_sellEOD = self.c_total_sellEOD + 1
        # the last element has already been initialised to 0.  modify it to the
        # sold amount
        self.sell_amount[-1] = sell_amount
        self.sell_EOD[-1] = "1"

        print_object = transaction(self.path_to_transaction_file)
        date = str(self.rowslist[index])[2:12]
        time = str(self.rowslist[index])[12:18]
        print_object.print_transaction_items(date, time, self.line[self.column_no_of_ticker], "0", str(bought),
                                             str(current_close_price),
                                             str(self.sell_amount[-1]), "3")

    '''
        self.transactions_file.writerow(str(self.rowslist[index])[2:12] +
                                        str(self.rowslist[index])[12:18] +
                                        self.line[0] + "0" + str(bought) + str(self.rowslist[index][2]) +
                                        str(sell_amount) + "1")
    '''
