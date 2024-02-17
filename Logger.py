import logging
import datetime


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

current_date_and_time = str(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))

file_handler = logging.FileHandler(f'{current_date_and_time.replace(" ", "_")}.log')

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def log(message):
    logger.info(message)
