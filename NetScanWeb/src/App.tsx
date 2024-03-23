import {useState} from "react";
import './App.css';
import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import Scanner from "./Scanner.tsx";
import AttacksAccordions from "./AttacksAccordions.tsx";
import Logs from "./Logs.tsx";
import { PieChart } from "./PieChart.tsx";
import Statistics from "./Statistics.tsx";


function App() {
  const [darkMode, setDarkMode] = useState('dark')

  const darkTheme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });
  return (
    <div>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline/>
        <Scanner/>
        <AttacksAccordions/>
        <Logs/>
      </ThemeProvider>
      <Statistics />
    </div>
  )
}



export default App;
