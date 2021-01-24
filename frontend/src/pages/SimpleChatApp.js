import "../styles/ChatApp.css";
import React, {useState, useEffect} from "react";
import {NetworkManager, Components} from "../react-chatbot-ui";

const SimpleChatApp = () => {

    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState(undefined);
    const uid = sessionStorage.getItem("uid");

    useEffect(() => {
            let elem = document.getElementById('messageList');
            elem.scrollTop = elem.scrollHeight;
    }, [messages])

    return (
        <>
            {!uid ?
                <div className={"login-container"}>
                    <label>Insert username and press enter</label>
                    <br/>
                    <form>
                        <input
                            className={"input"}
                            type={"text"}
                            onChange={e => sessionStorage.setItem("uid", e.target.value)}
                            placeholder={"Insert your username"}
                        />
                    </form>
                </div> :
                <NetworkManager
                    url={"ws://localhost:8765"}
                    uid={uid}
                    onMessage={(m) => setMessages([...messages, {from: "Chat", message: JSON.parse(m).utterance}])}
                    onOpen={() => setMessages([...messages, {from: "Socket", message: "Connection opened!"}])}
                    onClose={() => setMessages([...messages, {from: "Socket", message: "Connection closed!"}])}
                    onError={() => setMessages([...messages, {from: "Socket", message: "Error in connection!"}])}
                >
                    <div style={{
                        borderRadius: 10,
                        height: "100%",
                        width: "100%",
                        backgroundColor: "white",
                        marginBottom: 10,
                        border: '1px solid rgba(0, 0, 0, 0.25)',
                    }}
                    >
                        <div
                            style={{
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "space-between",
                                flex: 1,
                                height: "100vh",
                                boxShadow: "3px #9E9E9E",
                                shadowRadius: "3px",
                            }}
                        >
                            <div className='messages' style={{display: "flex"}} id='messageList'>
                                <ul style={{width: "100%"}}>
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
                            <Components.OnSubmit
                                stopPropagation
                                type={"utterance"}
                                payload={{data: message}}
                                onSend={() => setMessages([...messages, {from: "from-me", message}])}
                                onOpen={() => {}/*setMessages([...messages, {from: "Socket", message: message}])*/}
                            >
                                <form className={"input-container"}>
                                    <input
                                        className={"input"}
                                        type={"text"}
                                        onChange={e => setMessage(e.target.value)}
                                        placeholder={"Type message"}
                                    />
                                </form>
                            </Components.OnSubmit>
                        </div>
                    </div>
                </NetworkManager>
            }
        </>
    );
}

export default SimpleChatApp;

