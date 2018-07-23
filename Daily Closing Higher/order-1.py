import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="di0s4c0noemdxek7")


## This is the URL we are supposed to paste on the browser
## https://kite.trade/connect/login?api_key=di0s4c0noemdxek7&v=3

## After authentication (if needed) it will give a request token - which is
## needed to be used in the following api call.

data = kite.generate_session("5lzi06nU5YwcpO2OEM7uifssEf1ZlHh2", api_secret="u4i4h483ap3ngn8zwpsnk3l23vjgc0h3")

print(data)

kite.set_access_token(data['access_token'])

# Place an order
try:
    order_id = kite.place_order(tradingsymbol="INFY",
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=1,
                                order_type=kite.ORDER_TYPE_MARKET,
                                variety="regular",
                                product=kite.PRODUCT_NRML)

    logging.info("Order placed. ID is: {}".format(order_id))
except Exception as e:
    logging.info("Order placement failed: {}".format(e.message))

# Fetch all orders
kite.orders()
