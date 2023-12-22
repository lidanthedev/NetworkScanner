import json
import os
import datetime

DIR = "attacks"

def save_attack_data(data: dict[str, str]):
    file_name = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + "_0"

    files_exists_amount = 0
    # if file already exists add a number to the end of the file name
    while os.path.exists(f"./{DIR}/{file_name}.json"):
        # get file name till files_amounts
        file_name = file_name[:file_name.rfind("_")]

        file_name += f"_{files_exists_amount}"
        files_exists_amount += 1

    with open(f"./{DIR}/{file_name}.json", "w") as f:
        json.dump(data, f, indent=4)
