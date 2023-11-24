import { useState, useEffect } from "react";
import './App.css';

function App() {
  const [scannerState, setScannerState] = useState(false);
  const stateBtn: HTMLButtonElement = document.getElementById("stateBtn") as HTMLButtonElement;

  useEffect(() => {
    const fetchScannerState = async () => {
      const state = await getScannerState();
      setScannerState(state);
    };

    fetchScannerState();
  }, []);

  return (
    <>
      <h1>Toggle Scanner</h1>
      <button id="stateBtn" onClick={async () => {
        stateBtn.disabled = true;
        const state = await setScanner(!scannerState);
        setScannerState(state);
        stateBtn.disabled = false;
      }}>
      Scanner is now {scannerState ? "On" : "Off"}
    </button>
  </>
  )
}

async function setScanner(mode: boolean): Promise<boolean> {
  const response = await fetch('http://localhost:5000/setState', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ state: mode })
  });
  const data = await response.json();
  return data["state"];
}

async function getScannerState(): Promise<boolean> {
  const response = await fetch('http://localhost:5000/getState');
  const data = await response.json();
  return data["state"];
}

export default App;