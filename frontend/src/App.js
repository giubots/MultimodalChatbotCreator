import "./styles/ChatApp.css";
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
                setMessages([...messages, {fromMe: "", message: JSON.parse(m).utterance}]);
            }}
        >
                <div className={"header"}>
                    <div className='messages' id='messageList'>
                        <ul>
                            {messages.map((m, i) => {
                                return (
                                    <div key={i} className={`message ${m.fromMe}`}>
                                        <div className='username'>
                                            { m.fromMe? "You" : "Socket" }
                                        </div>
                                        <div className='message-body'>
                                            { m.message }
                                        </div>
                                    </div>
                                )
                            })}
                        </ul>
                    </div>
                </div>
                <footer className={"footer"}>
                    <OnSubmit
                        stopPropagation
                        id={"button-2"}
                        type={"data"}
                        payload={{data: message}}
                        onSend={() => setMessages([...messages, {fromMe: "from-me", message}])}
                    >
                        <div className={"input-container"}>
                            <input
                                className={"input"}
                                type={"text"}
                                onChange={e => setMessage(e.target.value)}
                                placeholder={"Type message"}
                            />
                            <button className={"send-button"}>
                                Send
                            </button>
                        </div>

                    </OnSubmit>
                </footer>
        </SocketManager>
    );
}

export default App;




