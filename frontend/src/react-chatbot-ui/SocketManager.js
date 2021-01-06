import React from "react";
import PropTypes from "prop-types";

export const SocketContext = React.createContext("");

export class SocketManager extends React.Component {
    constructor(props) {
        super(props);
        this.url = props.url;
        this.uid = props.uid;
        this.state = {
            interaction: null,
        };
    }

    componentDidMount() {
        this.connect();
    }

    wsUrl() {
        return encodeURI(
            `${this.url}?uid=${this.uid}`
            + (this.state.interaction? `&interaction=${this.state.interaction}` : "")
        );
    };

    connect() {
        if (this.props.useRest) {
            //TODO: implement REST adapter
        }
        else {
            this.ws = new WebSocket(this.wsUrl());
            this.ws.onmessage = (event) => {
                console.info("[SocketManager] New message:", event.data);
                if (!this.state.interaction) {
                    this.setState({interaction: event.data});
                    return;
                }
                this.props.onMessage && this.props.onMessage(event.data);
            }

            this.ws.onopen = (event) => {
                console.info("[SocketManager] Connection opened!", event);
                this.props.onOpen && this.props.onOpen(event);
            }

            this.ws.onerror = (event) => {
                console.error("[SocketManager] Error", event);
                this.props.onError && this.props.onError(event);
                throw event;
            }

            this.ws.onclose = (event) => {
                console.info("[SocketManager] Connection closed!", event);
                this.props.onClose && this.props.onClose(event);
                setTimeout(() => {
                    this.connect();
                }, 1000);
            }
            this.setState({
                wsInterface: {
                    send: (message) => this.__send(message),
                }
            });
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

SocketManager.propTypes = {
    url: PropTypes.string.isRequired,
    uid: PropTypes.string.isRequired,
    onMessage: PropTypes.func,
    onOpen: PropTypes.func,
    onError: PropTypes.func,
    onClose: PropTypes.func,
}

