import csv



# the list that contains the symbols for all the stocks that need to be downloaded
path_to_stock_master_list = "C:/Users/Rohit/Python_source_code/list of stocks/ind_niftyfmcglist.csv"

path_to_historical_data = "C:/Users/Rohit/Python_source_code/historical_stock_5_min_data/"

def get_data_from_master_list():
    max_price_volatility = 0.02
    max_deviation_from_open= 0.005
    max_volume_volatility = 2
    max_capital_for_single_buy=10000
    target_price=0.015

    overall_buy = 0
    overall_sell = 0
    c_overall_wins = 0
    c_overall_sellEOD = 0


    with open(path_to_stock_master_list, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line:
                with open(path_to_historical_data + line[2] + ".csv", 'r') as g:
                    print('\n',line[2])
                    rows = csv.reader(g)
                    rowslist = list(rows)
                    index = 1
                    open_price = 0.0
                    close_price = 0.0
                    index_open = 1
                    index_close = 1
                    c = 0
                    total_cost =0.0
                    total_sell = 0.0
                    date = '0'

                    # counters to keep track of the number of rejections, buys and sells
                    c_rejected_vol_volatility = 0
                    c_rejected_price_volatility = 0
                    c_buys = 0
                    c_wins = 0
                    c_soldEOD = 0

                    while index < len(rowslist):
                        row = rowslist[index]
                        if row[0][8:10] != date[6:8]:
                            bought=0
                            c=0
                            date = str(row[0])[2:10]
                            index_open=rowslist.index(row)
                            if (row[4] != "Open"):
                                open_price=float(row[4])
                        if date+" 10:00:00" in row[0]:
                            close_price = float(row[1])
                            index_close = rowslist.index(row)
                            c = 1
                        if date + " 11:" in row[0] and c == 0:
                            print("No data for stock " + line[2] + " on date " + str(rowslist[index_open])[2:12] + "\n")
                            c = 2
                        if c == 1:
                            # have a separate function to determine open
                            if 0 <= (close_price - open_price) / open_price <= max_deviation_from_open:
                                f = 0
                                sell = 0
                                i = index_open + 1
                                while i <= index_close:
                                    # check
                                    vol_high = (float(rowslist[i][2]) - float(rowslist[index_open][2])) / float(rowslist[index_open][2])
                                    vol_low = (float(rowslist[i][3]) - float(rowslist[index_open][3])) / float(rowslist[index_open][3])
                                    if abs(vol_high) > max_price_volatility or abs(vol_low) > max_price_volatility:
                                        print("Stock " + line[2] + " rejected on date " + str(rowslist[index_open])[2:12] + " due to price volatility\n")
                                        c_rejected_price_volatility = c_rejected_price_volatility + 1
                                        f = 1
                                        break
                                    if float(rowslist[i][5]) >= max_volume_volatility * float(rowslist[i - 1][5]):
                                        print("Stock " + line[2] + " rejected on date " + str(rowslist[i])[2:18] + " due to volume volatility\n")
                                        f = 1
                                        c_rejected_vol_volatility = c_rejected_vol_volatility + 1
                                        break
                                    i+=1
                                if f == 0:
                                   bought = int(max_capital_for_single_buy / float(rowslist[index_close][1]))
                                   if bought != 0:
                                       total_cost=total_cost+bought*close_price
                                       print("Stock " + line[2] + " bought " + str(bought) + " shares at " + rowslist[index_close][1] + " price at date " + str(rowslist[index_open])[2:12] + " at time "+ str(rowslist[index_close])[12:18]+"\n")
                                       c_buys = c_buys + 1
                                       overall_buy = overall_buy + total_cost
                                   else:
                                       print("Could not buy stock " + line[2] + " on date " + str(rowslist[index_open])[2:12] + " due to insufficient daily stock fund\n")
                                   
                                        
                            else:
                                 print("Stock price of " + line[2] + " fell or increased too much on date " + str(rowslist[index_open])[2:12] + "\n")
                            c = 2
                        if bought!=0:
                            per=(float(rowslist[index][2])-close_price)/close_price
                            if per>=target_price:
                                total_sell=total_sell+bought*float(rowslist[index][2])
                                print("Stock " + line[2] + " sold " + str(bought) + " shares at " + rowslist[index][2] + " price at date " + str(rowslist[index])[2:12] + " at time "+ str(rowslist[index])[14:18]+"\n")
                                bought=0
                                c_wins = c_wins + 1
                                overall_sell = overall_sell + total_sell
                                c_overall_wins = c_overall_wins + 1
                        if "15:15" in rowslist[index][0] and bought!=0:
                            total_sell=total_sell+bought*float(rowslist[index][1])
                            print("Stock " + line[2] + " sold " + str(bought) + " shares at " + rowslist[index][1] + " price at date " + str(rowslist[index])[2:12] + " at time "+ str(rowslist[index])[14:18]+"\n")
                            c_soldEOD = c_soldEOD + 1
                            overall_sell = overall_sell + total_sell
                            c_overall_sellEOD = c_overall_sellEOD + 1
                        index+=1
                    print("Total buy = "+str(total_cost)+" total sell = "+str(total_sell)+" and total profit = "+str(total_sell-total_cost)+ " for stock "+line[2]+"\n")
                    print("No of Wins = "+str(c_wins)+" No of EOD sell= "+str(c_soldEOD)+" Price vol rejections = "+str(c_rejected_price_volatility)+" Volume vol rejections = "+str(c_rejected_vol_volatility)+ " for stock "+line[2]+"\n")
    print("Ovearll buy = " + str(overall_buy) + " Overall sell = " + str(overall_sell) + " Overall wins = " + str(c_overall_wins) + " Overall sell EOD = " + str(c_overall_sellEOD))
get_data_from_master_list()
