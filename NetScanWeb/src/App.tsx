import { useState, useEffect } from "react";
import './App.css';
import CheckedAttacks from "./CheckedAttacks.tsx";
import NotificationsSender from "./NotificationsSender.tsx";
import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import Scanner from "./Scanner.tsx";
import AttacksAccordions from "./AttacksAccordions.tsx";
import AttackAccordion from "./AttackAccordion.tsx";

function App() {
  const [darkMode, setDarkMode] = useState('dark')

  const darkTheme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  const dummyAttackData = {
    "Attack_name": "DHCP SPOOFING",
    "Date": "04/01/2024",
    "IP": "10.0.0.16",
    "Is_Defended": false,
    "MAC": "58:6c:25:9e:cc:b2",
    "Time": "20:50:32",
    "WIFI": "Simion-Gaming"
  }

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline/>
      <AttackAccordion attackData={dummyAttackData} expanded={true} id={'hello'} handleChange={panel => event => {}}/>
    </ThemeProvider>
  )
}



export default App;
