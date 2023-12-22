import {useEffect, useState} from "react";

export default function CheckedAttacks() {

  const [checkedAttacks, setCheckedAttacks] = useState(<div></div>);

  useEffect(() => {
    fetch('http://localhost:5000/getAttacksState').then(response => response.json()).then(data => {
      const newCheckedAttacks = data.map((attack: any) => (
        <label style={{display: "flex"}}>
          <input
            type="checkbox"
            defaultChecked={attack["state"]}
            onChange={async (event) => {
              event.target.disabled = true;
              const isChecked = event.target.checked;
              await fetch('http://localhost:5000/setAttackState', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({id: attack["id"], state: isChecked})
              });
              event.target.disabled = false;
            }}
          />
          {attack["id"]}
        </label>
      ));

      setCheckedAttacks(newCheckedAttacks)
    });
  }, []);

  return (
    <div>
      {checkedAttacks}
    </div>
  )
}