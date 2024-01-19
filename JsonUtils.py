import json
import os.path

FILE_NAME = "attacks"


def save_attack_data(data: dict[str, str]):
    if not os.path.exists(f"./{FILE_NAME}.json"):
        with open(f"./{FILE_NAME}.json", "w") as f:
            json.dump([], f, indent=4)

    with open(f"./{FILE_NAME}.json", "r") as f:
        attacks = json.load(f)

    # convert data to list if not
    if type(attacks) is dict:
        attacks = [attacks]

    attacks.append(data)
    with open(f"./{FILE_NAME}.json", "w") as f:
        json.dump(attacks, f, indent=4)
