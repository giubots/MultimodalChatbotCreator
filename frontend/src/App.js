import "./styles/ChatApp.css";
import React, {useState} from "react";
import {OnSubmit, SocketManager} from "./react-chatbot-ui";

function App() {

    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState(undefined);
    const uid = sessionStorage.getItem("uid");

    return (
        <>
            {!uid?
                <div className={"login-container"}>
                    <label>Insert username and press enter</label>
                    <br />
                    <form>
                        <input
                            className={"input"}
                            type={"text"}
                            onChange={e => sessionStorage.setItem("uid", e.target.value)}
                            placeholder={"Insert your username"}
                        />
                    </form>
                </div> :
                <SocketManager
                    url={"ws://localhost:8765"}
                    uid={uid}
                    onMessage={(m) => setMessages([...messages, {from: "Chat", message: JSON.parse(m).utterance}])}
                    onOpen={() => setMessages([...messages, {from: "Socket", message: "Connection opened!"}])}
                    onClose={() => setMessages([...messages, {from: "Socket", message: "Connection closed!"}])}
                    onError={() => setMessages([...messages, {from: "Socket", message: "Error in connection!"}])}
                >
                    <div className={"page"}>
                        <div className={"col-left"}>

                        </div>
                        <div className={"col-right"}>
                            <div className={"header"}>
                                <div className='messages' id='messageList'>
                                    <ul>
                                        {messages.map((m, i) => {
                                            return (
                                                <div key={i} className={`message ${m.from}`}>
                                                    <div className='username'>
                                                        {m.from}
                                                    </div>
                                                    <div className='message-body'>
                                                        {m.message}
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
                                    type={"utterance"}
                                    payload={{data: message}}
                                    onSend={() => setMessages([...messages, {from: "from-me", message}])}
                                >
                                    <form className={"input-container"}>
                                        <input
                                            className={"input"}
                                            type={"text"}
                                            onChange={e => setMessage(e.target.value)}
                                            placeholder={"Type message"}
                                        />
                                        {/*<button className={"send-button"}>
                                            Send
                                        </button>*/}
                                    </form>

                                </OnSubmit>
                            </footer>
                        </div>
                    </div>
                </SocketManager>
            }
        </>
    );
}

export default App;




