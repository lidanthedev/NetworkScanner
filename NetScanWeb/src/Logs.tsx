import * as React from 'react';
import {useEffect, useState} from 'react';
import {Pagination} from "@mui/material";

function getAttacks() {
  return fetch('http://localhost:5000/logs').then(response => response.json());
}

export default function Logs() {
  const [expanded, setExpanded] = React.useState<string | false>(false);
  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState(0); // Add a state for the current page
  const itemsPerPage = 10; // Define how many items you want per page

  const handleChange =
    (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false);
    };

  useEffect(() => {
    getAttacks().then(attacks => setLogs(attacks));
  }, []);

  // Function to handle page change
  const handlePageChange = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>, newPage: number) => {
    setPage(newPage);
  };

  return (
    <div>
      <h3>Logs</h3>
      {logs.slice(page * itemsPerPage, (page + 1) * itemsPerPage).map((log, index) => {
        return (
          <div key={index}>
            <a href={`http://localhost:5000/log/${log}`}>{log}</a>
          </div>
        )
      })}
      <Pagination count={Math.floor(logs.length / itemsPerPage)} page={page} onChange={handlePageChange} />
    </div>
  );
}