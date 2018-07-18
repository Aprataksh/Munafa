import sys
sys.path.insert(0, r"..\utilities")
import requests
from dateutil import tz
import time, datetime
import csv, openpyxl
from config import config
import database
import pprint

# Get the token dictionary
def get_token_list(path_to_instrument_tokens):
    token_list = {}
    book = openpyxl.load_workbook(path_to_instrument_tokens)
    sheet = book["instrument_Modified"]
    for row in sheet.iter_rows(min_col=1, max_col=13):
        if row[12].value == "CURRENT" and row[0].value != "instrument_token":
            token_list[row[0].value] = row[2].value
    return token_list

def get_data(query_database, write_database):
    with open("%_min_candles.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date Time", "Ticker_Id", "High"])
        f.close()
    # Query for First Entry in Database
    initial_date_query = "SELECT first(price) FROM live_data"
    # Query for last Entry in Database
    final_date_query = "SELECT last(price) FROM live_data"
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    url_post = "http://localhost:8086/write"
    url_get = "http://localhost:8086/query"
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    payload = {
        'db': query_database,
        'q': initial_date_query,
        'precision': "s",
    }
    response = requests.request("GET", url_get, params=payload, headers=headers)
    data = response.json()
    # Date Time for First Entry in Database in UTC
    initial_date = data['results'][0]['series'][0]['values'][0][0]
    utc = datetime.datetime.strptime(initial_date, date_format)
    utc = utc.replace(tzinfo=tz.tzutc())
    # Date Time for First Entry in Database in Local
    initial_date = str(utc.astimezone(tz.tzlocal()))[:-6]
    # Timestamp for First Date Time Entry
    initial_timestamp = time.mktime(time.strptime(initial_date, "%Y-%m-%d %H:%M:%S"))
    print(initial_date, initial_timestamp)
    payload = {
        'db': query_database,
        'q': final_date_query,
        'precision': "s",
    }
    response = requests.request("GET", url_get, params=payload, headers=headers)
    data = response.json()
    # Date Time for Last Entry in Database
    final_date = data['results'][0]['series'][0]['values'][0][0]
    utc = datetime.datetime.strptime(final_date, date_format)
    utc = utc.replace(tzinfo=tz.tzutc())
    # Date Time for Last Entry in Database in Local
    final_date = str(utc.astimezone(tz.tzlocal()))[:-6]
    # Timestamp for Last Date Time Entry
    final_timestamp = time.mktime(time.strptime(final_date, "%Y-%m-%d %H:%M:%S"))
    print(final_date, final_timestamp)
    # Loop for candles starting from first to the last timestamp with "size_of_candle" seconds as gap
    for candles in range(int(initial_timestamp), int(final_timestamp), size_of_candle):
        # Query for maximum value of price, from live_data between "size_of_candle" seconds grouped by ticker_id
        payload = {
            'db': query_database,
            'q': f"SELECT max(price),min(price),last(price),first(price) FROM live_data WHERE time>={candles}s AND time<={candles + size_of_candle}s GROUP BY ticker_id",
            'precision': "s",
        }
        response = requests.request("GET", url_get, params=payload, headers=headers)
        data = response.json()
        #Condition if there is no data set for 5 minutes, if will take care of the 'series' error you were talking about
        if len(data['results'][0]) == 1:
            print("No data set found")
            continue
        data_values = data['results'][0]['series']
        final_payload = ""
        for value in data_values:
            start_time = datetime.datetime.fromtimestamp(candles)
            # Data values
            high = value['values'][0][1]
            low = value['values'][0][2]
            close = value['values'][0][3]
            open_val = value['values'][0][4]
            ticker = value['tags']['ticker_id']
            trading_symbol = token_list[int(ticker)]
            # WRITING TO THE .CSV FILE with start time of the candle, ticker_id and max_price of it in specific time
            with open("5_min_candles.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([start_time, ticker, trading_symbol, close, high, low, open_val])
            # Payload for each data entry in the database
            payload_post = f"live_data,ticker_id={ticker},trading_symbol={trading_symbol} high={high},low={low},close={close},open={open_val}"
            final_payload += payload_post + "\n"
        params = {'db': write_database, 'precision': 's'}
        # Post request for each candle
        post_response = requests.request("POST", url_post, data=final_payload, params=params)
        print(post_response)


obj = config("../config.txt")
path_to_instrument_list = obj.path_to_instrument_tokens()
token_list = get_token_list(path_to_instrument_list)

# SIZE OF THE CANDLE
size_of_candle = 300


def main():
    query_database = "CHECK_DATA_VOL"
    write_database = "OHLC_DATA" + "_" + str(size_of_candle)
    database.create_database(write_database)
    get_data(query_database, write_database)

main()
