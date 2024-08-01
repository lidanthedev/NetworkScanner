# Eilat-2004-NetworkScanner

## Mission 🎯

This project is a network scanner that detects and defends from MITM (Man in the middle) attacks including arp poisoning, dhcp spoofing, dns spoofing, evil twin, port scan

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

## Troubleshooting

NodeJS Engine not supported:
Install the latest version of NodeJS from the official website.
Or use [NVM (Node Version Manager)](https://github.com/nvm-sh/nvm) to install the latest version of NodeJS.

```bash
nvm install 21
```

Python Version not supported:
Install the latest version of Python from the official website.

If the program is crashed and your internet connection is not working run the following command:

```bash
sudo iptables -D INPUT 1
```

## Known Issues

* The program is not working on Windows.
* Google DNS may block the requests and it will show as an error.
