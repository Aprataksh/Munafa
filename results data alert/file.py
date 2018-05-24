import csv
import datetime
import requests
import codecs

weekday = int(datetime.date.today().strftime("%w"))
today = datetime.date.today().day
month = datetime.date.today().month
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def get_ticker_list_in_week():
    print('Scheduled in current week\n')
    page = requests.get(url)
    lines = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))
    for line in lines:
        if "Symbol" not in line and "Financial Results" in line[3] :
            str = line[4]
            intstr = int(str[0] + str[1])
            m = str[3:6]
            if m == months[month - 1] and 0 <= intstr - today <= 7 - weekday:
                print(line[0],'  ',line[1],'\n')

def get_ticker_list_in_month():
    print('\nScheduled in current month\n')
    url = 'https://www.nseindia.com/corporates/datafiles/BM_Latest_Announced.csv'
    page = requests.get(url)
    lines = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))
    for line in lines:
        if "Symbol" not in line and "Financial Results" in line[3] :
            str = line[4]
            intstr = int(str[0] + str[1])
            m = str[3:6]
            if m == months[month - 1]:
               print(line[0],'  ',line[1],'\n')

def get_same_ticker():
    tucker_list_temp = []
    print('\nCompanies that are common\n')
    with open(r"C:\Users\microsoft\Desktop\Stock Market\venv\symbols.csv",'r') as g:
        lines = csv.reader(g)
        for line in lines:
            tucker_list_temp.append(line[0])
    page = requests.get(url)
    lines = csv.reader(codecs.iterdecode(page.content.splitlines(), "utf-8"))
    for line in lines:
        if line[0] in tucker_list_temp :
            print(line[0]," ",line[4],'\n')

get_ticker_list_in_week()
get_ticker_list_in_month()
get_same_ticker()
url = 'https://www.nseindia.com/corporates/datafiles/BM_Latest_Announced.csv'
