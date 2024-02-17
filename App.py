import atexit
import json
import Logger

from flask import Flask, send_from_directory
from flask import request
from flask_cors import CORS

from Scanner import Scanner

app = Flask(__name__)
CORS(app, supports_credentials=True)

scanner = Scanner()
scanner.start()


@app.route("/setAttackState", methods=["POST"])
def set_attack_state():
    """
    Toggle the state of an attack.
    :return: The state of the attack.
    """
    data = request.get_json()
    attack_id = data["id"]
    state = data["state"]

    scanner.set_attack_state(attack_id, state)
    Logger.log(f"Attack {attack_id} state set to {state}")
    return {"id": attack_id, "state": state}


@app.route("/setState", methods=["POST"])
def toggle():
    """
    Toggle the state of the scanner.
    :return: The state of the scanner.
    """
    data = request.get_json()
    state = data["state"]

    if state != scanner.state:
        scanner.state = state
        if scanner.state == True:
            scanner.start()
        else:
            scanner.stop()
    return {"state": scanner.state}


@app.route("/getState")
def get_state():
    """
    Get the state of the scanner.
    :return: The state of the scanner.
    """
    return {"state": scanner.state}


@app.route("/getAttacksState")
def get_attacks_state():
    """
    Get the state of the attacks.
    :return: The state of the attacks.
    """
    return [{"id": handler.handler_id, "state": handler.state} for handler in scanner.handlers]


@app.route("/getNotifications")
def get_notifications():
    """
    Get the notifications from the scanner.
    :return: The notifications.
    """
    return scanner.get_notifications()


def exit_handler():
    """
    Stop the scanner when the program exits.
    :return: None
    """
    scanner.stop()


@app.route("/getAttacks")
def get_attacks():
    """
    Get the attacks from the file.
    :return: The attacks.
    """
    try:
        with open("attacks.json", "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return []


@app.route("/logs")
def logs():
    return Logger.get_all_logs_files()


@app.route("/log/<filename>")
def get_log(filename):
    return send_from_directory('logs', filename)


if __name__ == "__main__":
    atexit.register(exit_handler)
    app.run()
