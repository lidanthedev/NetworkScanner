import * as React from 'react';
import AttackAccordion, {AttackData} from "./AttackAccordion.tsx";
import {useEffect, useState} from "react";
import {Pagination} from "@mui/material";

function getAttacks() {
  return fetch('http://localhost:5000/getAttacks').then(response => response.json());
}

export default function AttacksAccordions() {
  const [expanded, setExpanded] = React.useState<string | false>(false);
  const [attacks, setAttacks] = useState([]);
  const [page, setPage] = useState(0); // Add a state for the current page
  const itemsPerPage = 10; // Define how many items you want per page

  const handleChange =
    (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false);
    };

  useEffect(() => {
    getAttacks().then(attacks => setAttacks(attacks));
  }, []);

  // Function to handle page change
  const handlePageChange = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>, newPage: number) => {
    setPage(newPage);
  };

  return (
    <div>
      <h3>Past Attacks</h3>
      {attacks.slice(page * itemsPerPage, (page + 1) * itemsPerPage).map((attack, index) => {
        return (
          <AttackAccordion
            key={index}
            attackData={attack}
            expanded={expanded === `${index}`}
            handleChange={handleChange}
            id={`${index}`}
          />
        )
      })}
      <Pagination count={Math.floor(attacks.length / itemsPerPage)} page={page} onChange={handlePageChange} />
    </div>
  );
}