'''
author: Aprataksh Anand
'''
import csv
import pandas as pd

def drop_extra_headers(path_to_historical_data, ticker):
    drop_index = []
    df = pd.read_csv(path_to_historical_data + ticker + ".csv")
    for i in df.index:
        if "Close" in df.values[i]:
            drop_index.append(i)
    if len(drop_index) > 0:
        df = df.drop(df.index[drop_index])
    return df

