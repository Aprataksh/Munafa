import csv
from datetime import datetime

class data_reader():

    trade_entry_rowslist = []
    trade_exit_rowslist = []
    trade_entry_index = 0
    trade_exit_index = 0
    entry_or_exit = False

    def get_row_for_trade_entry(self):
        row = []
        if self.trade_entry_index < len(self.trade_entry_rowslist):
            row = self.trade_entry_rowslist[self.trade_entry_index]
        return row

    def get_prev_row_for_trade_entry(self):
        row = []
        if self.trade_entry_index < len(self.trade_entry_rowslist):
            row = self.trade_entry_rowslist[self.trade_entry_index - 1]
        return row

    def get_row_for_trade_exit(self):
        row = []
        if self.trade_exit_index < len(self.trade_exit_rowslist):
            row = self.trade_exit_rowslist[self.trade_exit_index]
        return row

    def get_prev_row_for_trade_exit(self):
        row = []
        if self.trade_exit_index < len(self.trade_exit_rowslist):
            row = self.trade_exit_rowslist[self.trade_exit_index - 1]
        return row

    def move_to_next_row(self):
        if self.entry_or_exit == False:
            self.trade_entry_index = self.trade_entry_index + 1
        else:
            self.trade_exit_index = self.trade_exit_index + 1

    def find_date_in_date_list(self,date_to_find,search_start_index,date_list):
        date_to_find = datetime.strptime(date_to_find[2:], "%y-%m-%d %H:%M:%S")
        for i in range(search_start_index, len(date_list)):
            date = datetime.strptime(date_list[i][self.datetime_column][2:], "%y-%m-%d %H:%M:%S")
            if date_to_find <= date:
                return i
        return -1

    def init_trade_exit_index(self,date):
        self.trade_exit_index = self.find_date_in_date_list(date,1,self.trade_exit_rowslist)
        if self.trade_exit_index == -1:
            self.trade_exit_index = len(self.trade_exit_rowslist) - 1

    def init_trade_entry_index(self):
        self.trade_entry_index = self.find_date_in_date_list(self.trade_exit_rowslist[self.trade_exit_index][0],self.trade_entry_index,self.trade_entry_rowslist)
        if self.trade_entry_index == -1:
            self.trade_entry_index = len(self.trade_entry_rowslist) - 1

    def check_trade_exit_eof(self):
        if self.trade_exit_index == len(self.trade_exit_rowslist) - 1:
            return True
        else:
            return False

    def read_trade_entry_data(self):
        with open(self.obj.path_to_trade_entry_dir() + self.line[self.column_no_of_ticker] + ".csv", 'r') as g:
            self.trade_entry_rowslist = list(csv.reader(g))

    def read_trade_exit_data(self):
        with open(self.obj.path_to_trade_exit_dir() + self.line[self.column_no_of_ticker] + ".csv", 'r') as g:
            self.trade_exit_rowslist = list(csv.reader(g))
