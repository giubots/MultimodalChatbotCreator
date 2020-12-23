import React from "react";
import {SocketContext, useWebsocket} from './SocketManager';

class WebSocketComponent extends React.Component {
    static contextType = SocketContext;
    handleEvent(type) {
        const {id, payload} = this.props;
        const message = {
            id,
            type,
            payload,
        }
    }
}

export const OnClick = (props) => {

    function handleEvent(e, type, context) {
        props.stopPropagation && e.stopPropagation();
        const {id, payload} = props;
        const message = {
            id,
            type,
            payload,
        }
        context.send(JSON.stringify(message));
    }
    return (
        <SocketContext.Consumer>
            {context => {
                props.onEvent && props.onEvent(context.receive);
                    return (
                        <div
                            onClickCapture={(e) => {
                                handleEvent(e,"click", context);
                            }}
                        >
                            {props.children}
                        </div>
                    );
                }}
        </SocketContext.Consumer>
    );
}
