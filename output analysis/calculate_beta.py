import csv
import sys
import pandas as pd
import logging
from scipy.stats import linregress
sys.path.insert(0, r"../Utilities")
import config

class cal_risk():

    config_obj = config.config(r"../config.txt")
    col_obj = config.col_num(r"../config.txt")
    log_filename = "index.log"
    log_format = "%(levelname)s - %(message)s"
    logging.basicConfig(filename= config_obj.path_to_output_dir() + log_filename, level=logging.DEBUG, format=log_format,
                        filemode="w")
    logger = logging.getLogger()

    def __init__(self,path):
        self.path_to_transaction_file = path

    def calculate_per(self,data_list):
        per = 0.0
        per_list = []
        per_list.append(0)
        for i in range(1,len(data_list)):
            per = ((data_list[i] - data_list[i - 1]) / data_list[i - 1]) * 100
            per_list.append(per)
        return per_list

    def calculate_port(self,ticker,quant,date):
        vosp = 0
        with open(self.config_obj.path_to_historical_1_day_dir() + ticker + ".csv ", 'r') as g:
            data = csv.reader(g)
            for d in data:
                if date in d[0]:
                    vosp = quant * float(d[self.col_obj.get_close_col()])
        return vosp

    def calculate_slope(self,x,y):
        return linregress(x,y).slope

    def cal_risk(self):
        date_col = 0
        bal_col = 8
        sell_type_col = 3
        ticker_col = 2
        amt_col = 4
        sum = 0
        vosp = 0
        bal_list = []
        date_list = []
        holdings = []
        holdings_quant = []
        index_data_list = []
        per_data_list = []
        per_index_list = []
        start_date = ""
        end_date = ""
        s_d_i = 0
        e_d_i = 0
        prev_sum = 0
        vosp = 0
        slope = 0
        c = 0
        with open(self.path_to_transaction_file ,'r') as f:
            lines = list(csv.reader(f))
            start_date = lines[0][0]
            end_date = lines[len(lines) - 1][0]

        with open(self.config_obj.path_to_index_1_day_dir(),'r') as g:
                index_data = list(csv.reader(g))
                for i in index_data:
                    if 'Close' not in i:
                        date_list.append(i[self.col_obj.get_datetime_col()])
                        index_data_list.append(float(i[self.col_obj.get_close_col()]))
        s_d_i = date_list.index(start_date)
        e_d_i = date_list.index(end_date)
        date_list = date_list[s_d_i:e_d_i + 1]
        index_data_list = index_data_list[s_d_i:e_d_i + 1]
        for date in date_list:
            with open(self.path_to_transaction_file ,'r') as f:
                lines = list(csv.reader(f))
            for line in lines:
                if date[:10] in line[date_col]:
                    c = 1
                    if line[sell_type_col] == '1':
                        holdings_quant.append(line[amt_col])
                        holdings.append(line[ticker_col])
                    else:
                        holdings.reverse()
                        index = len(holdings) - holdings.index(line[ticker_col]) - 1
                        holdings.reverse()
                        holdings.pop(index)
                        holdings_quant.pop(index)
                if c == 1 and date not in line[date_col]:
                    c = 0
                    sum = float(lines[lines.index(line) - 1][bal_col])
                    break
            for i in range(0,len(holdings)):
                vosp = vosp + self.calculate_port(holdings[i],float(holdings_quant[i]),date)
            if sum == 0:
                sum = prev_sum
            prev_sum = sum
            sum = sum + vosp
            bal_list.append(float(sum))
            self.logger.debug("Date = " + date)
            self.logger.debug("Holdings list: ")
            for i in holdings:
                self.logger.debug(i)
            self.logger.debug("Balance = " + str(prev_sum))
            self.logger.debug("VOSP = " + str(vosp))
            self.logger.debug("Total value = " + str(sum) + "\n")
            sum = 0
            vosp = 0
        df = pd.DataFrame(bal_list,index=pd.DatetimeIndex(date_list, name='Date'),columns=['Balance'])
        df['Index'] = index_data_list
        per_data_list = self.calculate_per(bal_list)
        per_index_list = self.calculate_per(index_data_list)
        df['Balance per'] = per_data_list
        df['Index per'] = per_index_list
        slope = self.calculate_slope(per_index_list,per_data_list)
        print(df)
        print("Slope is = ",slope)
        self.logger.debug("Slope = " + str(slope))
        df.to_csv(self.config_obj.path_to_output_dir() + "Risk_calculation.csv")
def main():
    config_obj = config.config(r"../config.txt")
    obj = cal_risk(config_obj.path_to_ledger_list())
    obj.cal_risk()
main()
