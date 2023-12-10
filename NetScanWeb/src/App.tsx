import { useState, useEffect, useRef } from "react";
import './App.css';

function App() {
  const [scannerState, setScannerState] = useState(false);
  const stateBtnRef = useRef<HTMLButtonElement>(null);

  const [checkedAttacks, setCheckedAttacks] = useState([<div></div>]);
  
  
  
  useEffect(() => {
    const fetchScannerState = async () => {
      const state = await getScannerState();
      setScannerState(state);
    };

    const initCheckedAttacks = async () => {
      const response = await fetch('http://localhost:5000/getAttacksState');
      const data = await response.json();
      const newCheckedAttacks = data.map((attack: any) => (
        <label style={{ display: "flex" }}>
          <input
            type="checkbox"
            defaultChecked={attack["state"]}
            onChange={async (event) => {
              event.target.disabled = true;
              const isChecked = event.target.checked;
              const response = await fetch('http://localhost:5000/setAttackState', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: attack["id"], state: isChecked })
              });

              event.target.disabled = false;
            }}
          />
          {attack["id"]}
        </label>
      ));

      setCheckedAttacks(newCheckedAttacks);
    };

    fetchScannerState();
    initCheckedAttacks();
  }, []);

  return (
    <div>
      <h1>Toggle Scanner</h1>

      <button
        ref={stateBtnRef}
        onClick={async () => {
          if (stateBtnRef.current == null) {
            return;
          }
          stateBtnRef.current.disabled = true;
          const state = await setScanner(!scannerState);
          setScannerState(state);
          stateBtnRef.current.disabled = false;
        }}
      >
        Scanner is now {scannerState ? "On" : "Off"}
      </button>
      {checkedAttacks}
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
