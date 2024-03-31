# Eilat-2004-NetworkScanner

## Mission 🎯

This project is a network scanner to detect and defend from 

## Installation

### Requirements
* Linux
* [Python](https://www.python.org/downloads/) >= 3.10
* [NodeJS](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) >= 20

Install dependencies for Backend:
```bash
apt-get install build-essential python3-full python3-pip libnetfilter-queue-dev
pip install -r requirements.txt
```

Run the Backend:
```bash
sudo -E python3 App.py
```


Frontend:
now open a second terminal in the same working directory and run the following commands:
```bash
cd NetScanWeb
npm i
npm run dev
```

## Usage
Open your browser and go to `http://localhost:5173`
There you can manage the network scanner and see the results.