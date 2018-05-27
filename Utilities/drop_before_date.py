'''
author: Aprataksh Anand
'''
import pandas as pd

def drop_before_date(data, final_date):
    date_data = data['Date Time'].tolist()
    #date = "2018-04-10"
    index = 0
    for date in date_data:
        if final_date in date:
            index = date_data.index(date)
            break
    if index == 0:
        print("drop_before_date: no such date")
    else:
        data = data.drop(data.index[[range(0, index)]])
    return data
'''
def main():
    df = pd.read_csv(r"C:/Users/Hp/Desktop/New folder/Top500_stock/Date Time Data/" + "3MINDIA" + ".csv")
    print(drop_data(df))
main()
'''