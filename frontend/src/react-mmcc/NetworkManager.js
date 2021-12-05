/**
 * NetworkManager library.
 * This file contains the network wrapper that add the
 * connection layer.
 *
 * @version 1.0.1
 * @author [Davide Savoldelli](https://github.com/savdav96)
 */

import React, {createContext} from "react";
import PropTypes from "prop-types";

export const NetworkContext = createContext({});

/**
 * The NetworkManager must be set as parent of all component which
 * need a connection layer.
 */
export class NetworkManager extends React.Component {
    constructor(props) {
        super(props);
        this.url = props.url;
        this.uid = props.uid;
        this.state = {
            interaction: null,
            interface: {},
        };
    }

    componentDidMount() {
        this.connect();
    }

    wsUrl() {
        return encodeURI(
            `${this.url}/use/${this.uid}`
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
                this.setState({
                    interface: {
                        ...this.state.interface,
                        onMessage: event.data,
                    }
                });
                this.props.onMessage && this.props.onMessage(event.data);
            }

            this.ws.onopen = (event) => {
                console.info("[SocketManager] Connection opened!", event);
                this.props.onOpen && this.props.onOpen(event);
                this.setState({
                    interface: {
                        ...this.state.interface,
                        onOpen: event,
                    }
                });
            }

            this.ws.onerror = (event) => {
                console.error("[SocketManager] Error", event);
                this.props.onError && this.props.onError(event);
                this.setState({
                    interface: {
                        ...this.state.interface,
                        onError: event,
                    }
                });
            }

            this.ws.onclose = (event) => {
                console.info("[SocketManager] Connection closed!", event);
                this.props.onClose && this.props.onClose(event);
                this.setState({
                    interface: {
                        ...this.state.interface,
                        onClose: event,
                    }
                });
                /*setTimeout(() => {
                    this.connect();
                }, 1000);*/
            }
            this.setState({
                interface: {
                    ...this.state.interface,
                    send: (message) => this.__send(message),
                }
            });
        }
    }

    __send(message) {
        if (this.ws) {
            try {
                this.ws.send(message);
            } catch (error) {
                console.error("[SocketManager] Error in sending the message", error);
            }
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
            <NetworkContext.Provider
                value={this.state.interface}
            >
                {this.props.children}
            </NetworkContext.Provider>
        )
    }
}

NetworkManager.propTypes = {
    /**
     * The url of the connection.
     * It supports WebSocket protocol.
     * In future it will handle HTTP connections with REST api's.
     */
    url: PropTypes.string.isRequired,
    /**
     * The unique identifier of the connection
     * Must be pre-shared before connecting.
     */
    uid: PropTypes.string.isRequired,
    /**
     * A callback function which triggers the receive event.
     * @param: {Object} event The message received.
     */
    onMessage: PropTypes.func,
    /**
     * A callback function which triggers the open event.
     * @param: {Object} event The received open event.
     */
    onOpen: PropTypes.func,
    /**
     * A callback function which triggers the error event.
     * @param: {Object} event The received error event.
     */
    onError: PropTypes.func,
    /**
     * A callback function which triggers the close event.
     * @param: {Object} event The received close event.
     */
    onClose: PropTypes.func,
    /**
     * A boolean which toggles the ability to use REST
     * HTTP protocol instead of WebSocket. Not yet implemented.
     */
    useRest: PropTypes.bool,
}


