import logo from './logo.svg';
import './App.css';
import React from "react";
import {OnClick, OnSubmit, SocketManager} from "./react-chatbot-ui";

function App() {

  return (
      <SocketManager url={"ws://localhost:8765"}>
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo"/>
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
            <OnClick
                id={"button-1"}
                stopPropagation
                onEvent={e => console.log("[Button 1] Received from server:", e)}
                payload={{
                  data: "button-1",
                }}
            >
              <div onClick={() => alert("should not work")}>Button 1</div>
            </OnClick>

            <OnClick
                id={"button-2"}
                onEvent={e => console.log("[Button 2] Received from server:", e)}
                payload={{
                  data: "button-2",
                }}
            >
              <button onClick={() => alert("should work")}>Button 2</button>
            </OnClick>
            <OnSubmit>
                <input type={"text"} name={"nome"} />
                <input type={"text"} name={"cognome"} />
                <input type={"text"} name={"indirizzo"} />
                <input type={"text"} name={"città"} />
                <input type={"submit"} />
            </OnSubmit>

            <OnSubmit type={"utterance"}>
                <input type={"text"} />
                <input type={"submit"} />
            </OnSubmit>

            <OnClick
                id={"button-3"}
                onEvent={e => console.log("[Button 3] Received from server:", e)}
                payload={{data: "button-3",}}
            >
              <div onClick={() => alert("should work")}>Button 3</div>
            </OnClick>
          </header>
        </div>
      </SocketManager>
  );
}

export default App;




