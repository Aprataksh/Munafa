import requests
from dateutil import tz
import time, datetime
import pprint

def create_database(database_name):
    url = "http://localhost:8086/query"
    payload = "q=CREATE%20DATABASE%20" + database_name
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

def send_data(database_name, data):
    url = "http://localhost:8086/write"
    final_payload = ""
    for token in data:
        print(token)
        ticker_no = token['instrument_token']
        price = token["last_price"]
        payload = f"live_data,ticker_id={ticker_no} price={price}"
        final_payload += payload + "\n"
    params = {'db': database_name, 'precision': 's'}
    response = requests.request("POST", url, data=final_payload, params=params)
    print(response)
    return

def get_data():
    url = "http://localhost:8086/query"
    payload = {
        'db': "CHECK_DATA",
        'q': "SELECT * FROM \"live_data\"",
        'precision': "s",
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    response = requests.request("GET", url, params=payload, headers=headers)
    data = response.json()
    values = data['results'][0]['series'][0]['values']
    print("Timestamp\t\t\t\tTicker_No\tClosing Price")
    for value in values:
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        utc = datetime.datetime.strptime(value[0], date_format)
        utc = utc.replace(tzinfo=tz.tzutc())
        local = str(utc.astimezone(tz.tzlocal()))[:-6]
        print(local, "\t", value[2], "\t", value[1])

def main():
    #database_name = "CHECK_DATA"
    #data = [100, 10]
    #create_database(database_name)
    #send_data(database_name, data)
    get_data()