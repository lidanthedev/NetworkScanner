from flask import Flask
from flask import request

from Scanner import Scanner

app = Flask(__name__)

scanner = Scanner()


@app.route("/toggle")
def toggle():
    if scanner.state == True:
        scanner.stop()
    else:
        scanner.start()
    return str(scanner.state)


@app.route("/getState")
def getState():
    return str(scanner.state)


if __name__ == "__main__":
    app.run()
