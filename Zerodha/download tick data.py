from kiteconnect import KiteTicker
import kiteconnect
import openpyxl

import sys
import database
sys.path.insert(0, "../Utilities")
from config import zerodha_tokens, config
import csv

# TOKENS USING CONFIG OBJECT
config_object = zerodha_tokens("../config.txt")
api_key = config_object.get_zerodha_api_key()
public_token = config_object.get_zerodha_public_token()
api_secret = config_object.get_zerodha_api_secret()


config_obj = config("../config.txt")
path_to_instrument_tokens = config_obj.path_to_instrument_tokens()
# Please enter the user ID here before executing the script
# user_id = ""

# CREATING DATABASE
database.create_database("CHECK_DATA")

"""with open("ticks.csv", "w", newline="") as f:
    f.close()"""


# EXTRACTING TOKEN LIST
def get_token_list():
    token_list = []
    book = openpyxl.load_workbook(path_to_instrument_tokens)
    sheet = book["Sheet1"]
    for row in sheet.iter_rows(min_col=1, max_col=13):
        if row[12].value == "CURRENT" and row[0].value != "instrument_token":
            token_list.append(row[0].value)
    return token_list


token_list = get_token_list()

# KITE-CONNECT
kite = kiteconnect.KiteConnect(api_key=api_key)
data = kite.generate_session(public_token, api_secret=api_secret)
access_token = data['access_token']
kite.set_access_token(access_token)
kws = KiteTicker(api_key, access_token)

# COLLECTING TICKS
def on_ticks(ws, ticks):
    # SENDING VALUES TO DATABASE
    database.send_data("CHECK_DATA", ticks)
    """# WRITING TO THE .CSV FILE
    with open("ticks.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([len(ticks), ticks])"""

# CONNECTING
def on_connect(ws, response):
    ws.subscribe(token_list)
    ws.set_mode(ws.MODE_LTP, token_list)


kws.on_ticks = on_ticks
kws.on_connect = on_connect

kws.connect()