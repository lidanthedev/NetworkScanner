import {useState} from "react";
import './App.css';
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
      <Scanner/>
      <AttacksAccordions/>
    </ThemeProvider>
  )
}



export default App;
