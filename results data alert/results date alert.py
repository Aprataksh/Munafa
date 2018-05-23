import csv
import datetime

ticker_list_in_week = []
weekday = int(datetime.date.today().strftime("%w"))
today = datetime.date.today().day
month = datetime.date.today().month
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def get_ticker_list_in_week():
    with open(r"C:\Users\microsoft\Desktop\Stock Market\venv\BM_Latest_Announced.csv",'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line and "Financial Results" in line[3] :
                str = line[4]
                intstr = int(str[0] + str[1])
                m = str[3:6]
                if m == months[month - 1] and 0 <= intstr - today <= 7 - weekday:
                    ticker_list_in_week.append(line[0])
    print("Scheduled in current week\n",ticker_list_in_week,'\n')

ticker_list_in_month = []
def get_ticker_list_in_month():
    with open(r"C:\Users\microsoft\Desktop\Stock Market\venv\BM_Latest_Announced.csv",'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if "Symbol" not in line and "Financial Results" in line[3] :
                str = line[4]
                intstr = int(str[0] + str[1])
                m = str[3:6]
                if m == months[month - 1]:
                    ticker_list_in_month.append(line[0])
    print("Scheduled in current month\n",ticker_list_in_month)

def get_same_ticker():
    tucker_list_temp = []
    print()
    with open(r"C:\Users\microsoft\Desktop\Stock Market\venv\symbols.csv",'r') as g:
        lines = csv.reader(g)
        for line in lines:
            tucker_list_temp.append(line[0])
    with open(r"C:\Users\microsoft\Desktop\Stock Market\venv\BM_Latest_Announced.csv",'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if line[0] in tucker_list_temp :
                print(line[0]," ",line[4],'\n')

get_ticker_list_in_week()
get_ticker_list_in_month()
get_same_ticker()
