import React from "react";

export const SocketContext = React.createContext("");

export class SocketManager extends React.Component {
    constructor(props) {
        super(props);
        this.url = props.url

        this.state = {
            wsInterface: {
                send: (message) => this.__send(message),
                receive: "No messages yet",
            },
            interaction: "None",
        };
    }

    componentDidMount() {
        this.connect();
    }

    connect() {
        if (this.props.useRest) {
            //TODO: implement REST adapter
        }
        else {
            this.ws = new WebSocket(this.url + `?uid="Davide"` + `&interaction=${this.state.interaction}`);
            this.ws.onmessage = (event) => {
                if (this.state.interaction === "None") {
                    this.setState({interaction: event.data});
                    return;
                }
                console.info("[SocketManager] New message:", event.data);
                const wsInterface = {
                    send: (message) => this.__send(message),
                }
                this.props.onReceive && this.props.onReceive(event.data);
                this.setState({ wsInterface });
            }

            this.ws.onopen = (event) => {
                console.info("[SocketManager] Connection opened!", event.data);
            }

            this.ws.onerror = (event) => {
                console.error("[SocketManager] Error", event);
                throw event;
            }

            this.ws.onclose = (event) => {
                console.debug("[SocketManager] Connection closed!");
                setTimeout(() => {
                    this.connect();
                }, 1000);
            }
        }
    }

    __send(message) {
        if (this.ws) {
            this.ws.send(message);
        }
    }

    componentWillUnmount () {
        try {
            this.ws !== null && this.ws.close();
        } catch (error) {
            console.error("[SocketManager] Error in unmounting", error);
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

