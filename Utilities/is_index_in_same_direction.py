import pandas as pd
import csv
import datetime
import logging
import config

def is_index_in_same_direction(path_to_index_file, direction, final_date_time):

    config_object = config.config("../config.txt")
    path_to_output_dir = config_object.path_to_output_dir()

    log_filename = "index.log"
    log_format = "%(levelname)s - %(message)s"
    logging.basicConfig(filename= path_to_output_dir + log_filename, level=logging.DEBUG, format=log_format,
                        filemode="w")
    logger = logging.getLogger()

    data = pd.read_csv(path_to_index_file)
    date_data = data['Date Time'].tolist()
    final_date = final_date_time[:10]
    found = 0
    initial_index = 0
    for index in range(len(date_data)):
        if final_date == date_data[index][:10]:
            initial_index = index
            found = 1
            break
    if found == 0:
        logger.info("is_index_in_same_direction: no such date: " + str(final_date_time))
        return False
    else:
        open_price = data['Close'][initial_index]
        index = initial_index
        found = 0
        while index < len(date_data):
            if final_date_time in date_data[index]:
                found = 1
                close_price = data['Close'][index]
                logger.info("Date: " + final_date_time + " Index Close price: " + str(close_price) + " Index Open price: " + str(open_price) + "\n")
                if direction == 1:
                    if close_price >= open_price:
                        return True
                    else:
                        logger.info("Date: " + final_date_time + " Index not in the same direction")
                        return False
                else:
                    if close_price < open_price:
                        return True
                    else:
                        logger.info("Date: " + final_date_time + " Index not in the same direction")
                        return False
            index = index + 1
        if found == 0:
            logger.info("No index data for " + final_date_time)
def main():
    final_date = "2018-05-25 10:30"
    direction = 1
    val = is_index_in_same_direction("NIFTY.csv", direction, final_date)
    print("Return = " + str(val))