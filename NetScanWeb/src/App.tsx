import { useState, useEffect } from "react";
import './App.css';
import CheckedAttacks from "./CheckedAttacks.tsx";

function App() {
  const [scannerState, setScannerState] = useState(false);

  useEffect(() => {
    getScannerState().then(state => setScannerState(state));
  }, []);

  return (
    <div>
      <h1>Toggle Scanner</h1>

      <button
        onClick={async (event) => {
          if (!(event.target instanceof HTMLButtonElement)) {
            return
          }
          event.target.disabled = true;
          const state = await setScanner(!scannerState);
          setScannerState(state);
          event.target.disabled = false;
        }}
      >
        Scanner is now {scannerState ? "On" : "Off"}
      </button>

      <CheckedAttacks />
    </div>
  );
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
