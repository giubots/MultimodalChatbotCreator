import React from "react";
import {SocketContext} from './SocketManager';

function handleEvent(event, context, props, payload, text) {
    let message = {
        type: props.type || event.type,
    }
    if (props.type === "utterance") {
        message["utterance"] = text;
    } else {
        message["payload"] = payload || props.payload;
    }
    props.stopPropagation && event.stopPropagation();
    props.onSend && props.onSend(message);
    context.send(JSON.stringify(message));
}

export const OnClick = (props) => {
    return (
        <SocketContext.Consumer>
            {(context) => {
                return (
                    <div
                        onClick={(e) => {
                            handleEvent(e, context, props)
                        }}
                    >
                        {props.children}
                    </div>
                );
            }}
        </SocketContext.Consumer>
    );
}


export const OnSubmit = (props) => {
    return (
        <SocketContext.Consumer>
            {(context) => {
                return (
                    <div
                        onSubmit={(e) => {
                            e.preventDefault();
                            console.log(e);
                            let payload = {};
                            let text;

                            // Framework compliant utterance type
                            if (props.type === "utterance") {
                                text = e.target[0].value;
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
                            handleEvent(e, context, props, payload, text);
                            e.target.reset();
                        }}
                    >
                        {props.children}
                    </div>
                );
            }}
        </SocketContext.Consumer>
    );
}
