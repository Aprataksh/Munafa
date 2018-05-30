import pandas as pd
import csv
import datetime

def is_index_in_same_direction(path_to_index, direction, final_date):
    data = pd.read_csv(path_to_index)
    date_data = data['Date Time'].tolist()
    index = 0
    for date in date_data:
        if final_date in date:
            index = date_data.index(date)
            break
    if index == 0:
        print("is_index_in_same_direction: no such date")
    else:
        open_price = data['Close'][index]
        while True:
            index = index + 1
            if final_date + " 10:00:00" in date_data[index]:
                close_price = data['Close'][index]
                print("Date: " + date + " Index Close price: " + str(close_price) + " Index Open price: " + str(open_price) + "\n")
                if direction == 1:
                    if (close_price > open_price):
                        return True
                    else:
                        print("Date: " + date + " Index not in the same direction")
                        return False
                else:
                    if (close_price <  open_price):
                        return True
                    else:
                        print("Date: " + date + " Index not in the same direction")
                        return False
            if final_date not in date_data[index]:
                print("Moved to next date")
                break

'''
def main():
    #df = pd.read_csv(r"C:/Users/Hp/Desktop/New folder/Top500_stock/Date Time Data/" + "3MINDIA" + ".csv")
    path_to_index = "C:/Users/Rohit/Python_source_code/historical_indices_5_min_data/CNXFMCG.csv"
    final_date = "2018-05-25"
    direction = 1
    val = is_index_in_same_direction(path_to_index, direction, final_date)
    print("Return = " + str(val))
main()
'''