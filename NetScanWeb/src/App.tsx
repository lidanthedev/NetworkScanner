import {useState} from "react";
import './App.css';
import {createTheme, CssBaseline, ThemeProvider} from "@mui/material";
import Scanner from "./Scanner.tsx";
import AttacksAccordions from "./AttacksAccordions.tsx";
import Logs from "./Logs.tsx";
import { PieChart } from "./PieChart.tsx";

const data = [
  { name: "Mark", value: 90 },
  { name: "Robert", value: 12 },
  { name: "Emily", value: 34 },
  { name: "Marion", value: 53 },
  { name: "Nicolas", value: 98 },
]

function App() {
  const [darkMode, setDarkMode] = useState('dark')

  const darkTheme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });
  return (
    // <ThemeProvider theme={darkTheme}>
    //   <CssBaseline/>
    //   <Scanner/>
    //   <AttacksAccordions/>
    //   <Logs/>
    // </ThemeProvider>
    <PieChart data={data} width={400} height={400} />
  )
}



export default App;
