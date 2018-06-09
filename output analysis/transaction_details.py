import csv
import time
import pandas as pd
import sys
sys.path.insert(0, r"..\utilities")
from ledger import ledger
import logging
class transaction():
    def __init__(self, ptt ,ptll):
        self.path_to_transaction_list = ptt
        self.path_to_ledger_log = ptll
        log_format = "%(levelname)s - %(message)s"
        logging.basicConfig(filename=self.path_to_ledger_log, level=logging.DEBUG, format=log_format, filemode="w")
        self.logger = logging.getLogger()

    """Function that gets epoch time and also sorts the data to a .csv file"""

    def get_sorted_data(self, ptsd):
        self.path_to_sorted_data = ptsd
        with open(self.path_to_sorted_data, 'w') as f:
            f.close()

        with open(self.path_to_transaction_list, 'r') as f:
            self.lines = csv.reader(f)
            for self.line in self.lines:
                date = self.line[0] + self.line[1]
                pattern = "%Y-%m-%d %H:%M"
                timestamp = time.mktime(time.strptime(date, pattern))
                self.line.insert(0, timestamp)
                with open(self.path_to_sorted_data, 'a', newline="") as w:
                    writer = csv.writer(w)
                    writer.writerow(self.line)

        df = pd.read_csv(self.path_to_sorted_data, header=None, index_col=False)
        df_list = df.columns.values.tolist()
        df = df.sort_values(by=df_list[0])
        del df[df_list[0]]
        df.to_csv(self.path_to_sorted_data, header=None, index=None)
        self.logger.info("Sorted File Created")

    """Function for getting the transaction details according to the balance"""

    def max_capital_required(self, ptsd, ptlf):
        self.path_to_sorted_data = ptsd
        self.path_to_ledger_file = ptlf
        with open(self.path_to_ledger_file, "w") as f:
            f.close()

        initial_balance = 30000
        balance = 30000
        '''
        initial_balance = 100000
        balance = 100000'''
        self.ledger_obj = ledger(balance, self.path_to_ledger_file)
        min = balance
        with open(self.path_to_sorted_data, "r") as f:
            self.lines = list(csv.reader(f))
            for self.line in self.lines:
                if self.line[3] == "1":
                    purchase = float(self.line[6])
                    if self.ledger_obj.is_required_capital_available(purchase):
                        balance = self.ledger_obj.debit(self.line)

                    else:
                        index = self.lines.index(self.line)
                        ticker = self.lines[index][2]
                        self.logger.info("Cannot Buy at = " + str(self.line) + " At Index = " + str(index + 1))
                        i = 1
                        while index + i < len(self.lines):
                            if self.lines[index + i][2] == ticker and self.lines[index + i][3] == '0':
                                self.logger.info("Cannot Sell = " + str(self.lines[index + i]) + " At Index = " + str(index + i + 1))
                                #Deletes the entry in the list of transactions, so that it is not sold
                                del self.lines[index + i]
                                break
                            i = i + 1

                else:
                    sale = float(self.line[6])
                    balance = self.ledger_obj.credit(self.line)
                if min > balance:
                    min = balance
            self.logger.info("Profit = " + str(self.ledger_obj.profit()))
            self.logger.info("Maximum Capital Required = " + str(initial_balance - min))


def main():

    # # path_to_transaction_list = r"C:\Users\Hp\Desktop\New folder\transactions.csv"
    # path_to_sorted_data = r"C:\Users\Hp\Desktop\New folder\sorted_transactions.csv"
    # path_to_ledger_file = r"C:\Users\Hp\Desktop\New folder\ledger.csv"
    # path_to_ledger_log = r"C:\Users\Hp\Desktop\New folder\ledger.log"

    path_to_transaction_list = r"C:\Users\Rohit\Python_source_code\output\daily_closing_higher\transactions.csv"
    path_to_sorted_data = r"C:\Users\Rohit\Python_source_code\output\daily_closing_higher\sorted_transactions.csv"
    path_to_ledger_file = r"C:\Users\Rohit\Python_source_code\output\daily_closing_higher\ledger.csv"
    path_to_ledger_log = r"C:\Users\Rohit\Python_source_code\output\daily_closing_higher\ledger.log"

    obj = transaction(path_to_transaction_list, path_to_ledger_log)
    obj.get_sorted_data(path_to_sorted_data)
    obj.max_capital_required(path_to_sorted_data, path_to_ledger_file)
main()