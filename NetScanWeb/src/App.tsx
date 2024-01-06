import { useState, useEffect } from "react";
import './App.css';
import CheckedAttacks from "./CheckedAttacks.tsx";
import NotificationsSender from "./NotificationsSender.tsx";
import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import Scanner from "./Scanner.tsx";
import AttacksAccordions from "./AttacksAccordions.tsx";

function App() {
  const [darkMode, setDarkMode] = useState('dark')

  const darkTheme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline/>
      <AttacksAccordions/>
    </ThemeProvider>
  )
}



export default App;
