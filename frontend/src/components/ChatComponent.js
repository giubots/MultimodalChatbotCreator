import {Icon} from "semantic-ui-react";
import React, {useState, useEffect} from "react";
import "../styles/Chat.css";
import {Components} from "../react-mmcc";

export const ChatComponent = ({messagesProps, setMessagesProps}) => {
    const [visible, setVisible] = useState(false);
    const [messages, setMessages] = useState([]);
    const [message, setMessage] = useState(undefined);
    let messagesList = null;

    useEffect(() => {
        setMessages(messagesProps);
        if (messagesList) {
            messagesList.scrollTop = messagesList.scrollHeight;
        }
    }, [messagesProps, messagesList, messages])

    return (
        <div style={styles.overlay}>
            {visible && (
                <div style={styles.outerContainer}>
                    <div style={styles.innerContainer}>
                        <div
                            ref={r => messagesList = r}
                            className='messages'
                            style={{display: "flex"}}>
                            <ul style={{width: "100%", paddingInlineStart: 0}}>
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
                            onSend={() => setMessagesProps([...messages, {from: "from-me", message}])}
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
                style={{
                    boxShadow: "0px 4px 13px 6px rgba(0,0,0,0.20)",
                }}
            />
        </div>
    );
}

const styles = {
    overlay: {
        elevation: 5,
        position: "absolute",
        bottom: 0,
        right: 0,
        margin: 30,
        display: "flex",
        alignItems: "flex-end",
        flexDirection: "column",
    },
    outerContainer: {
        borderRadius: 10,
        height: 700,
        width: 500,
        marginBottom: 10,
        border: '1px solid rgba(0, 0, 0, 0.25)',
        boxShadow: "0px 4px 30px 6px rgba(0,0,0,0.20)",
    },
    innerContainer: {
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        flex: 1,
        height: 700,
        boxShadow: "3px #9E9E9E",
        shadowRadius: "3px",
    }
}
