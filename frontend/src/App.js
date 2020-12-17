import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react";
import { onClick, ws, receive } from "./react-chatbot-ui";

function App() {
  const [currentTime, setCurrentTime] = useState(0);
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");

  useEffect(() => {
    /*fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });*/

  }, []);

  let e = receive();
  console.log(e);

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
        <onClick id={"button-1"}>
          <div onClick={() => alert("should not work")}>Button 1</div>
        </onClick>
        <onClick id={"button-2"}>
          <button onClick={() => alert("should not work")}>Button 2</button>
        </onClick>
        <onClick id={"button-3"}>
          <div onClick={() => alert("should not work")}>Button 3</div>
        </onClick>

        <p>Example of usage of ws: {output}</p>
        <input name={""} onChange={(event) => setInput(event.target.value)}/>
        <button onClick={() => {
          ws.send(input);
        }}>Submit</button>
        <p>Flask server time: {currentTime}</p>
      </header>
    </div>
  );
}

export default App;




