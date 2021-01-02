import React, {useContext} from "react";
import {SocketContext} from './SocketManager';

function handleEvent (event, context, props, payload) {
    const message = {
        id: props.id,
        type: props.type || event.type,
        payload: payload || props.payload,
    }
    props.stopPropagation && event.stopPropagation();
    props.onSend && props.onSend(message);
    context.send(JSON.stringify(message));
}


const WebSocketComponent = (props) => {
    return (
        <SocketContext.Consumer>
            {() => {
                return <>{props.children}</>;
            }}
        </SocketContext.Consumer>
    );
}

export const OnClick = (props) => {
    const context = useContext(SocketContext)

    return (
        <WebSocketComponent>
            <div
                onClick={(e) => {handleEvent(e, context, props)}}
            >
                {props.children}
            </div>
        </WebSocketComponent>
    );
}


export const OnSubmit = (props) => {
    const context = useContext(SocketContext)

    return (
        <WebSocketComponent onReceive={props.onReceive}>
            <form
                action={"."}
                onSubmitCapture={(e) => {
                    e.preventDefault();

                    let payload = {};

                    // Framework compliant utterance type
                    if (props.type === "utterance") {
                        payload["text"] = e.target[0].value;
                    }

                    // Standard OnSubmit type
                    else {
                        for (let i = 0; i < e.target.length; i++) {
                            let t = e.target[i];
                            if (t.name) {
                                payload[t.name] = t.value;
                            }
                        }
                    }
                    handleEvent(e, context, props, payload);
                    return false;
                }}
            >
                {props.children}
            </form>
        </WebSocketComponent>
    );
}
