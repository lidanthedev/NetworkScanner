import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import './App.css';

function App() {
  const [scannerState, setScannerState] = useState(false);

  useEffect(() => {
    const fetchScannerState = async () => {
      const state = await toggleScanner();
      setScannerState(state);
    };

    fetchScannerState();
  }, []);

  return (
    <>
      <h1>Toggle Scanner</h1>
      <button onClick={async () => {
        const state = await toggleScanner();
        setScannerState(state);
      }}>
      Scanner is now {scannerState ? "On" : "Off"}
    </button>
  </>
  )
}

async function toggleScanner(): Promise<boolean> {
  const response = await fetch('http://localhost:5000/toggle');
  const data = await response.json();
  return data["state"];
}

async function getScannerState(): Promise<boolean> {
  const response = await fetch('http://localhost:5000/getState');
  const data = await response.json();
  return data["state"];
}

export default App;