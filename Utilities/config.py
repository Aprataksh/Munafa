import ast

class config():
    # the time after which we cease any buy or sell transaction
    trading_closing_time = "15:00"
    purchase_cutoff_time = "05:00 pm"

    def __init__(self, path_to_config):
        with open(path_to_config, "r") as f:
            dictionary = ast.literal_eval(f.read())
            self.historical_5_dir = dictionary.get("path_to_historical_5_dir")
            self.master_list = dictionary.get("path_to_master_list")
            self.output_dir = dictionary.get("path_to_output_dir")
            self.index_dir = dictionary.get("path_to_index_dir")
            self.transaction_list = dictionary.get("path_to_transaction_list")
            self.sorted_list = dictionary.get("path_to_sorted_list")
            self.ledger_list = dictionary.get("path_to_ledger_list")
            self.ledger_log = dictionary.get("path_to_ledger_log")
            self.historical_1_day_dir = dictionary.get("path_to_historical_1_day_dir")
            self.index_1_day_dir = dictionary.get("path_to_index_1_day_data")

    def path_to_historical_5_min_dir(self):
        return self.historical_5_dir
    def path_to_master_list(self):
        return self.master_list
    def path_to_index_dir(self):
        return self.index_dir
    def path_to_output_dir(self):
        return self.output_dir
    def path_to_transaction_list(self):
        return self.transaction_list
    def path_to_sorted_list(self):
        return self.sorted_list
    def path_to_ledger_list(self):
        return self.ledger_list
    def path_to_ledger_log(self):
        return self.ledger_log
    def path_to_historical_1_day_dir(self):
        return self.historical_1_day_dir
    def path_to_index_1_day_dir(self):
         return self.index_1_day_dir

class col_num():
    def __init__(self, path_to_config):
        with open(path_to_config, "r") as f:
            dictionary = ast.literal_eval(f.read())
            self.datetime_column = dictionary.get("datetime_column")
            self.close_column = dictionary.get("close_column")
            self.high_column = dictionary.get("high_column")
            self.low_column = dictionary.get("low_column")
            self.open_column = dictionary.get("open_column")
            self.scanner_ticker_column = dictionary.get("scanner_ticker_column")
            self.master_list_ticker_column = dictionary.get("master_list_ticker_column")

    def get_datetime_col(self):
        return self.datetime_column

    def get_close_col(self):
        return self.close_column

    def get_high_col(self):
        return self.high_column

    def get_low_col(self):
        return self.low_column

    def get_open_col(self):
        return self.open_column

    def get_scanner_ticker_col(self):
        return self.scanner_ticker_column

    def get_master_list_ticker_col(self):
        return self.master_list_ticker_column

class brokerage():
    # the charges are mentioned at https://zerodha.com/charges
    def __init__(self):
        # brokerage charges
        self.delivery_purchase_stt = 0.001
        self.delivery_sell_stt = 0.001
        self.max_intraday_brokerage = 20
        self.intraday_purchase_brokerage = 0.0001
        self.intraday_sell_stt = 0.00025
        self.intraday_purchase_stt = 0
        self.transaction = 0.00000325
        self.gst = 0.18

    def calculate_delivery_brokerage(self, sell_amount):
        brokerage_charges = 0
        # at present, we consider the taxes on the by amount to be the same  as the sale amount.  In reality,
        # if we are selling at a profit,  the taxes on the buy amount will be less. tto implement this, we will have to
        # also keep a track of the corresponding purchases and  sales  which is a TODO

        buy_amount = sell_amount
        stt = sell_amount * self.delivery_purchase_stt +\
                        buy_amount * self.delivery_purchase_stt
        transaction_charges = self.transaction * (sell_amount + buy_amount)
        gst = self.gst * (brokerage_charges + stt + transaction_charges)
        total_charges = brokerage_charges  + stt + transaction_charges + gst
        return total_charges

    def calculate_intraday_brokerage(self, sell_amount):
        # at present, we consider the taxes on the by amount to be the same  as the sale amount.  In reality,
        # if we are selling at a profit,  the taxes on the buy amount will be less. tto implement this, we will have to
        # also keep a track of the corresponding purchases and  sales  which is a TODO.
        buy_amount = sell_amount

        purchase_brokerage = min(self.max_intraday_brokerage, self.intraday_purchase_brokerage * buy_amount)
        sell_brokerage = min(self.max_intraday_brokerage, self.intraday_purchase_brokerage * sell_amount)

        brokerage_charges = purchase_brokerage + sell_brokerage

        stt = sell_amount * self.intraday_sell_stt+\
                        buy_amount * self.intraday_purchase_stt
        transaction_charges = self.transaction * (sell_amount + buy_amount)
        gst = self.gst * (brokerage_charges + stt + transaction_charges)
        total_charges = brokerage_charges  + stt + transaction_charges + gst
        return total_charges

class zerodha_tokens():
    def __init__(self, path_to_config_file):
        with open(path_to_config_file, "r") as f:
            dictionary = ast.literal_eval(f.read())
            self.zerodha_api_key = dictionary.get("zerodha_api_key")
            self.zerodha_api_secret = dictionary.get("zerodha_api_secret")
            self.zerodha_public_token = dictionary.get("zerodha_public_token")

    def get_zerodha_api_key(self):
        return self.zerodha_api_key

    def get_zerodha_api_secret(self):
        return self.zerodha_api_secret

    def get_zerodha_public_token(self):
        return self.zerodha_public_token
def main():
    path_to_config_file = r"../config.txt"
    obj = config()
