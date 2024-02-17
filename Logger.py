import datetime
import logging
import os


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            return f'\033[94m{super().format(record)}\033[0m'  # Blue color
        return super().format(record)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

current_date_and_time = str(datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S"))

if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = logging.FileHandler(f'logs/{current_date_and_time.replace(" ", "_")}.log')

file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(ColoredFormatter())

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def log(message):
    logger.info(message)


def get_all_logs_files():
    files_list = []
    for file in os.listdir('logs'):
        files_list.append(file)

    return files_list
