import {useState} from "react";
import {NativeSelect} from "@mui/material";

const MODES = ["PROTECT", "DETECT", "OFF"];

export default function SelectAttack(props: {attack: any}) {
  const [state, setState] = useState(MODES[0]);
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    setLoading(true);
    setAttackState(props.attack["id"], event.target.value);
    setLoading(false);
  }

  function setAttackState(attackId: string, value: string) {
    fetch('http://localhost:5000/setAttackState', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({id: attackId, state: value})
    }).then(r => r.json()).then(data => {
      setState(data["state"]);
    });
  }


  return (
    <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
      <div>
        {props.attack["id"]}
      </div>
      <NativeSelect readOnly={loading} value={state} onChange={(e) => handleChange(e)}>
        {MODES.map((mode) => (
          <option key={mode} value={mode}>
            {mode}
          </option>
        ))}
      </NativeSelect>
    </div>
  )
}