import logo from './logo.svg';
import './App.css';
import React, {useState} from "react";
import {OnSubmit, SocketManager} from "./react-chatbot-ui";

function App() {

    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState(undefined);

    return (
        <SocketManager
            url={"ws://localhost:8765"}
            onReceive={(m) => {
                console.log("[App] Received:", m)
                setMessages([...messages, m]);
            }}
        >
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
                    <div>
                        <h4>Text messages:</h4>
                        <ul>
                            {messages.map((m, i) => {
                                return <li key={i}><span>{m}</span></li>
                            })}
                        </ul>
                    </div>
                    <OnSubmit
                        id={"button-2"}
                        type={"data"}
                        payload={{data: message}}
                        onSend={() => setMessages([...messages, message])}
                    >
                        <input type={"text"} onChange={e => setMessage(e.target.value)}/>
                        <button>Send Message</button>
                    </OnSubmit>
                </header>
            </div>
        </SocketManager>
    );
}

export default App;




