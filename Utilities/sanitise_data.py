'''
author: Aprataksh Anand
'''
import drop_extra_headers
import drop_before_date

def sanitise_data(path_to_historical_data, ticker, date):
    data = drop_extra_headers.drop_extra_headers(path_to_historical_data, ticker)
    data = drop_before_date.drop_before_date(data, date)
    return data
