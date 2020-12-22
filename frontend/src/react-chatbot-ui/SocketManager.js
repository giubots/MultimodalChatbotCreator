import React from "react";

export const SocketContext = React.createContext("");
export const useWebsocket = () => React.useContext(SocketContext);

export class SocketManager extends React.Component {
    constructor(props) {
        super(props);
        this.url = props.url
        this.state = {
            lastMessage: "",
        }
    }

    componentDidMount() {
        this.connect();
    }

    connect() {
        this.ws = new WebSocket(this.url);
        this.ws.onmessage = (event) => {
            console.log(event);
            this.setState({
                lastMessage: event.data,
            });
        }

        this.ws.onopen = (event) => {
            console.debug("Connection opened!", event);
        }

        this.ws.onerror = (event) => {
            console.error("Error", event);
            throw event;
        }

        this.ws.onclose = (event) => {
            console.debug("Connection closed!", event);
            setTimeout(() => {
                this.connect();
            }, 1000);
        }

        this.wsInterface = {
            send: (message) => this._send(message),
            receive: () => this._receive(),
        }

        this.setState({
            wsInterface: this.wsInterface,
        })
    }

    _send(message) {
        if (this.ws) {
            this.ws.send(message);
        }
    }

    _receive() {
        return this.state.lastMessage;
    }

    componentWillUnmount () {
        try {
            this.ws !== null && this.ws.close();
        } catch (e) {
            console.error(e);
        }
    }

    render() {
        return (
            <SocketContext.Provider
                value={this.state.wsInterface}
            >
                {this.props.children}
            </SocketContext.Provider>
        )
    }
}

