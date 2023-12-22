from flask import Flask
from flask import request
from flask_cors import CORS

from Scanner import Scanner

app = Flask(__name__)
CORS(app)

scanner = Scanner()
scanner.start()

@app.route("/setAttackState", methods=["POST"])
def toggle_attack_state():
    data = request.get_json()
    attack_id = data["id"]
    state = data["state"]

    scanner.set_attack_state(attack_id, state)
    print(f"Attack {attack_id} state set to {state}")
    return {"id": attack_id, "state": state}



@app.route("/setState", methods=["POST"])
def toggle():
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
def getState():
    return {"state": scanner.state}

@app.route("/getAttacksState")
def getAttacksState():
    return [{"id": handler.handler_id, "state": handler.enabled} for handler in scanner.handlers]


if __name__ == "__main__":
    app.run()
