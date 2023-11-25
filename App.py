from flask import Flask
from flask import request
from flask_cors import CORS

from Scanner import Scanner

app = Flask(__name__)
CORS(app)

scanner = Scanner()


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


if __name__ == "__main__":
    app.run()
