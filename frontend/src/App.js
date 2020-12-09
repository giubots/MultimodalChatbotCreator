import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react";
import { Clickable } from "./react-chatbot-ui";

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <Clickable>
          <div onClick={() => alert("should not work")}>Ciao</div>
        </Clickable>

        <p>Flask server time: {currentTime}</p>
      </header>
    </div>
  );
}

export default App;




