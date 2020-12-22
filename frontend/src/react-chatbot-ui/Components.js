import React from "react";
import { SocketContext } from './SocketManager';

class WebSocketComponent extends React.Component {
    static contextType = SocketContext;
    handleEvent(type) {
        const {id, payload} = this.props;
        const message = {
            id,
            type,
            payload,
        }
        this.context?.send(JSON.stringify(message));
    }
}

export class OnClick extends WebSocketComponent {
    componentDidUpdate() {
        this.props.onEvent && this.props.onEvent(this.context?.receive());
    }

    render() {
        return (
            <div
                onClickCapture={(e) => {
                    this.props.stopPropagation && e.stopPropagation();
                    this.handleEvent("click");
                }}
            >
                {this.props.children}
            </div>
        );
    }
}
