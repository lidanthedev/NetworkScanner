import {useEffect, useState} from "react";
import SelectAttack from "./SelectAttack.tsx";

interface AutocompleteOption {
  label: string;
}
const MODES = ["PROTECT", "ON", "OFF"];

export default function CheckedAttacks() {

  const [checkedAttacks, setCheckedAttacks] = useState(<div></div>);

  useEffect(() => {
    fetch('http://localhost:5000/getAttacksState').then(response => response.json()).then(data => {
      const newCheckedAttacks = data.map((attack: any) => (
        <SelectAttack attack={attack} key={attack["id"]}/>
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