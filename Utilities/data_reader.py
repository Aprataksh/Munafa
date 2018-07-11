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
            row = self.trade_entry_rowslist[self.trade_entry_index-1]
        return row
    def get_row_for_trade_exit(self):
        row = []
        if self.trade_exit_index < len(self.trade_exit_rowslist):
            row = self.trade_exit_rowslist[self.trade_exit_index]
        return row
    def get_prev_row_for_trade_exit(self):
        row = []
        if self.trade_exit_index < len(self.trade_exit_rowslist):
            row = self.trade_exit_rowslist[self.trade_exit_index-1]
        return row
    def move_to_next_row(self):
        if self.entry_or_exit == False:
            self.trade_entry_index = self.trade_entry_index + 1
        else:
            self.trade_exit_index = self.trade_exit_index + 1
    def init_trade_exit_index(self,date):
        trade_entry_time = datetime.strptime(date[2:], "%y-%m-%d %H:%M:%S")
        for i in range(1,len(self.trade_exit_rowslist)):
            trade_exit_time = datetime.strptime(self.trade_exit_rowslist[i][self.datetime_column][2:], "%y-%m-%d %H:%M:%S")
            if trade_entry_time <= trade_exit_time:
                self.trade_exit_index = i
                break
    def init_trade_entry_index(self):
        trade_entry_time = datetime.strptime(self.trade_entry_rowslist[self.trade_entry_index][self.datetime_column][2:], "%y-%m-%d %H:%M:%S")
        trade_exit_time = datetime.strptime(self.trade_exit_rowslist[self.trade_exit_index][self.datetime_column][2:], "%y-%m-%d %H:%M:%S")
        while trade_entry_time < trade_exit_time:
            self.trade_entry_index = self.trade_entry_index + 1
            if self.trade_entry_index >= len(self.trade_entry_rowslist):
                break
            trade_entry_time = datetime.strptime(self.trade_entry_rowslist[self.trade_entry_index][self.datetime_column][2:], "%y-%m-%d %H:%M:%S")
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
