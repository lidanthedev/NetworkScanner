from flask import Flask
from flask import request
from flask_cors import CORS

from Scanner import Scanner

app = Flask(__name__)
CORS(app)

scanner = Scanner()


@app.route("/toggle")
def toggle():
    if scanner.state == True:
        scanner.stop()
    else:
        scanner.start()
    
    return {"state": scanner.state}


@app.route("/getState")
def getState():
    return {"state": scanner.state}


if __name__ == "__main__":
    app.run()
