import {Icon} from "semantic-ui-react";
import React, {useState} from "react";
import "../styles/ChatApp.css";
import {Components, NetworkManager} from "../react-chatbot-ui";

export const ChatComponent = () => {
    const [visible, setVisible] = useState(false);
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState(undefined);

    return (<div style={{
        elevation: 5,
        position: "absolute",
        bottom: 0,
        right: 0,
        margin: 30,
        display: "flex",
        alignItems: "flex-end",
        flexDirection: "column",
    }}>
        {visible && (<div style={{
            borderRadius: 10,
            height: 700,
            width: 500,
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
                             height: 700,
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
        </div>)
        }
        <Icon
            onClick={() => setVisible(!visible)}
            circular
            inverted
            color={'teal'}
            size={"big"}
            name='chat'
        />
    </div>);
}
