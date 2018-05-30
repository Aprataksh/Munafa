import csv
import sys
sys.path.insert(0, r"..\utilities")
import is_index_in_same_direction

class OHL():
    rowslist=[]
    line=[]
    total_cost=0.0
    total_sell=0.0
    total_purchased=0
    total_sold=0
    overall_cost=0.0
    overall_sell=0.0
    overall_c_wins = 0
    overall_c_sellEod = 0
    c_total_sellEOD = 0
    c_total_wins = 0

    def __init__(self, mpv, mdfo, mvv, mcfsb, tp):
        self.max_price_volatility = mpv
        self.max_deviation_from_open = mdfo
        self.max_volume_volatility = mvv
        self.max_capital_for_single_buy = mcfsb
        self.target_price = tp

    def check_price_volatility(self,index_open,index_close):
        i = index_open + 1
        while i <= index_close:
            vol_high = (float(self.rowslist[i][2]) - float(self.rowslist[index_open][2])) / float(self.rowslist[index_open][2])
            vol_low = (float(self.rowslist[i][3]) - float(self.rowslist[index_open][3])) / float(self.rowslist[index_open][3])
            if abs(vol_high) > self.max_price_volatility or abs(vol_low) > self.max_price_volatility:
                print("Stock " + self.line[2] + " rejected on date " + str(self.rowslist[index_open])[2:18] + " due to price volatility\n")
                return True
            i+=1
        return False

    def check_volume_volatility(self,index_open,index_close):
        i = index_open + 1
        while i <= index_close:
            if float(self.rowslist[i][5]) >= self.max_volume_volatility * float(self.rowslist[i - 1][5]):
                print("Stock " + self.line[2] + " rejected on date " + str(self.rowslist[i])[2:18] + " due to volume volatility\n")
                return True
            i+=1
        return False

    def buy_stocks(self,purchase_cost,index_close):
        bought = int(self.max_capital_for_single_buy / purchase_cost)
        if bought != 0:
            self.total_cost = self.total_cost + bought * purchase_cost
            self.total_purchased+=bought
            self.overall_cost+=self.total_cost
            print("Stock " + self.line[2] + " bought " + str(bought) + " shares at " + str(purchase_cost) + " price at date " + str(self.rowslist[index_close])[2:12] + " at time " + str(self.rowslist[index_close])[12:18] + "\n")
        else:
            print("Could not buy stock " + self.line[2] + " on date " + str(self.rowslist[index_open])[2:12] + " due to insufficient daily stock fund\n")
        return bought

    def sell_stock_due_to_price_check(self,bought,close_price,index):
        per = (float(self.rowslist[index][2]) - close_price) / close_price
        if per >= self.target_price:
            self.total_sell = self.total_sell + bought * float(self.rowslist[index][2])
            self.overall_sell+=self.total_sell
            self.total_sold+=bought
            print("Stock " + self.line[2] + " sold " + str(bought) + " shares at " + self.rowslist[index][2] + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[14:18] + "\n")
            self.overall_c_wins = self.overall_c_wins + 1
            self.c_total_wins = self.c_total_wins + 1
            return True
        return False

    def sell_stock_at_end_of_day(self,index,bought):
        self.total_sold+=bought
        self.total_sell = self.total_sell + bought * float(self.rowslist[index][1])
        self.overall_sell+=self.total_sell
        print("Stock " + self.line[2] + " sold " + str(bought) + " shares at " + self.rowslist[index][1] + " price at date " + str(self.rowslist[index])[2:12] + " at time " + str(self.rowslist[index])[14:18] + "\n")
        self.overall_c_sellEod = self.overall_c_sellEod + 1
        self.c_total_sellEOD = self.c_total_sellEOD + 1
    def OHL(self):
        # the list that contains the symbols for all the stocks that need to be downloaded
        path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/ind_niftyfmcglist.csv"

        path_to_historical_data = "C:/Users/Rohit/Python_source_code/historical_stock_5_min_data/"

        path_to_index_file = "C:/Users/Rohit/Python_source_code/historical_indices_5_min_data/CNXFMCG.csv"

        with open(path_to_stock_master_list, 'r') as f:
            self.lines = csv.reader(f)
            for self.line in self.lines:
                    if "Symbol" not in self.line:
                        with open(path_to_historical_data + self.line[2] + ".csv", 'r') as g:
                            print('\n',self.line[2])
                            rows = csv.reader(g)
                            self.rowslist = list(rows)
                            index = 1
                            open_price = 0.0
                            close_price = 0.0
                            index_open = 1
                            index_close = 1
                            c = 0
                            self.total_cost = 0.0
                            self.total_sell = 0.0
                            self.c_total_wins = 0
                            self.c_total_sellEOD = 0
                            date = '0'
                            while index < len(self.rowslist):
                                row = self.rowslist[index]
                                if 'Close' in row:
                                    index+=1
                                    continue
                                if row[0][8:10] != date[6:8]:
                                    bought = 0
                                    c = 0
                                    date = str(row[0])[2:10]
                                    index_open = index
                                    open_price = float(row[4])
                                if date + " 10:00:00" in row[0]:
                                    close_price = float(row[1])
                                    index_close = index
                                    c = 1
                                if date + " 11:" in row[0] and c == 0:
                                    print("No data for stock " + self.line[2] + " on date " + str(row)[2:12] + "\n")
                                    c = 2
                                if c == 1:
                                    if 0 <= ((close_price - open_price) / open_price) <= self.max_deviation_from_open:
                                        f = 0
                                        if self.check_price_volatility(index_open,index_close): 
                                            f = 1
                                        if self.check_volume_volatility(index_open,index_close):
                                            f = 1
                                        if is_index_in_same_direction.is_index_in_same_direction(path_to_index_file, 1, date):
                                            f = 1

                                        if f == 0:
                                            bought=self.buy_stocks(close_price,index_close)
                                    else:
                                            print("Stock price of " + self.line[2] + " fell or increased too much on date " + str(row)[2:12] + "\n")
                                    c = 2
                                if bought != 0:
                                    if self.sell_stock_due_to_price_check(bought,close_price,index):
                                        bought=0
                                if "15:15" in self.rowslist[index][0] and bought != 0:
                                    self.sell_stock_at_end_of_day(index,bought)
                                index+=1
                            print("Total buy = " + str(self.total_cost) + " total sell = " + str(self.total_sell) + " and total profit = " + str(self.total_sell - self.total_cost) + " for stock " + self.line[2] + "\n")
                            print("Total wins = " + str(self.c_total_wins) + " Total sell EOD = " + str(self.c_total_sellEOD))
        print("Total purchases = "+str(self.total_purchased)+" total sold = "+str(self.total_sold)+"\n")
        print("Overall cost = "+str(self.overall_cost)+" Overall sell = "+str(self.overall_sell)+"\n")
        print("Overall wins = " + str(self.overall_c_wins) + " Total sell EOD = " + str(self.overall_c_sellEod))
def main():
    max_price_volatility = 0.02
    max_deviation_from_open= 0.005
    max_volume_volatility = 2
    max_capital_for_single_buy=10000
    target_price=0.015

    obj=OHL(max_price_volatility,max_deviation_from_open,max_volume_volatility,max_capital_for_single_buy,target_price)
    obj.OHL()

main()
