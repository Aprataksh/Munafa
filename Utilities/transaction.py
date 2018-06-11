import csv


class transaction():
    def __init__(self, pttf):
        self.path_to_transaction_file = pttf

    def print_transaction_items(self, date, time, ticker, type, number, price, amount, sell_type):
        with open(self.path_to_transaction_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, time, ticker, type, number, price, amount, sell_type])
