import csv
class ledger():

    def __init__(self, mc, ptlf):
        self.path_to_ledger_file = ptlf
        self.max_capital = mc
        self.balance = mc

    def is_required_capital_available(self, reqd_capital):
        if self.balance > reqd_capital:
            return True
        else:
            return False

    def credit(self, rowlist):
        # Sanity check: balance should not exceed maximum capital
        credit_amount = float(rowlist[6])
        self.balance = round(self.balance + credit_amount, 2)
        rowlist.append(self.balance)
        with open(self.path_to_ledger_file, "a", newline="") as creditor:
            credit_writer = csv.writer(creditor)
            credit_writer.writerow(rowlist)
        return self.balance

    def debit(self, rowlist):
        # sanity check: balance should not fall below minimum of which is zero
        debit_amount = float(rowlist[6])
        if (self.balance - debit_amount) < 0:
            print("Error: balance less then minimum which is zero")
            print("balance : " + str(self.balance) + "debit amount: " + str(debit_amount))

        self.balance = round(self.balance - debit_amount, 2)
        rowlist.append(self.balance)
        with open(self.path_to_ledger_file, "a", newline="") as debitor:
            debit_writer = csv.writer(debitor)
            debit_writer.writerow(rowlist)
        return self.balance
    def profit(self):
        self.profit_amount = self.balance - self.max_capital
        return self.profit_amount