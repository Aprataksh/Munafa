from kiteconnect import KiteTicker, KiteConnect
import pprint
import sys
sys.path.insert(0, "../Utilities")
from config import zerodha_tokens

# TOKENS USING CONFIG OBJECT
config_object = zerodha_tokens("../config.txt")

api_key = config_object.get_zerodha_api_key()
public_token = config_object.get_zerodha_public_token()
api_secret = config_object.get_zerodha_api_secret()

# KITE-CONNECT
kite = KiteConnect(api_key=api_key)
data = kite.generate_session(public_token, api_secret=api_secret)

access_token = data['access_token']
kite.set_access_token(access_token)

kws = KiteTicker(api_key, access_token)

# Gets the holdings
holdings = kite.holdings()

# Example of holdings
"""holdings = [{'average_price': 153.1375,
             'close_price': 129.35,
             'collateral_quantity': 0,
             'collateral_type': '',
             'day_change': 0,
             'day_change_percentage': 0,
             'exchange': 'NSE',
             'instrument_token': 54273,
             'isin': 'INE208A01029',
             'last_price': 129.35,
             'pnl': -7611.999999999998,
             'price': 0,
             'product': 'CNC',
             'quantity': 320,
             'realised_quantity': 320,
             't1_quantity': 0,
             'tradingsymbol': 'ASHOKLEY'}]"""

instrument_token = []
purchase_price = {}
quantity = {}

# Gets the instrument token and purchase price for each holding
for holding in holdings:
    instrument = "NSE:" + holding['tradingsymbol']
    instrument_token.append(instrument)
    purchase_price[instrument] = holding['average_price']
    quantity[instrument] = holding['quantity']

# Gets the last trading price
ltp_prices = kite.ltp(instrument_token)
pprint.pprint(ltp_prices)

# Check for each instrument token
for token in instrument_token:
    percent_less_check = -0.03
    percent_less_sell = -0.05
    if ltp_prices[token]['last_price'] - purchase_price[token] < percent_less_check * purchase_price[token]:
        print("Less than 3 percent, token = ", token[4:], "\nLast Traded Price", ltp_prices[token]['last_price'],
                                                          "\nPurchase Price", purchase_price[token])

        # Commented so that while testing, orders don't get placed.
        """try:
            order_id = kite.place_order(tradingsymbol=token[4:]
                                        price=(1 + percent_less_sell) * purchase_price[token]
                                        exchange=kite.EXCHANGE_NSE,
                                        transaction_type=kite.TRANSACTION_TYPE_SELL,
                                        quantity=quantity[token],
                                        order_type=kite.ORDER_TYPE_LIMIT,
                                        variety="regular",
                                        product=kite.PRODUCT_NRML)
            print("Order placed. ID is: {}".format(order_id))
        except Exception as e:
            print("Order placement failed: {}".format(e.message))"""

kite.orders()

