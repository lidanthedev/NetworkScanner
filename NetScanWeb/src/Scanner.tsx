import CheckedAttacks from "./CheckedAttacks.tsx";
import NotificationsSender from "./NotificationsSender.tsx";
import {useEffect, useState} from "react";

export default function Scanner() {
  const [scannerState, setScannerState] = useState(false);


  useEffect(() => {
    getScannerState().then(state => setScannerState(state));
  }, []);

  return (
    <div>
      <h1>Network Scanner</h1>

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

      <CheckedAttacks/>
      <NotificationsSender/>
    </div>
  );
}

async function setScanner(mode: boolean): Promise<boolean> {
  const response = await fetch('http://localhost:5000/setState', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({state: mode})
  });
  const data = await response.json();
  return data["state"];
}

async function getScannerState(): Promise<boolean> {
  const response = await fetch('http://localhost:5000/getState');
  const data = await response.json();
  return data["state"];
}