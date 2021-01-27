/**
 * Components library.
 * This file contains all wrappers to be added to the pre-existing
 * ui elements in order to add network functionalities.
 *
 * @version 1.1.0
 * @author [Davide Savoldelli](https://github.com/savdav96)
 */

import React, {useEffect, useContext} from "react";
import {NetworkContext} from './NetworkManager';
import PropTypes from "prop-types";

function handleEvent(event, context, props, payload, text) {
    let message = {
        type: props.type || event.type,
    }
    if (props.type === "utterance") {
        message["utterance"] = text;
    } else {
        message["payload"] = props.payload || payload;
    }
    props.onSend && props.onSend(message);
    context.send(JSON.stringify(message));
}

function setUpProps(props, context) {
    const {onMessage, onOpen, onClose, onError} = context;
    props.onMessage && props.onMessage(onMessage)
    props.onError && props.onError(onError)
    props.onOpen && props.onOpen(onOpen)
    props.onClose && props.onClose(onClose)
}

/**
 * The onClick component handles all click events passed through its children.
 */
const OnClick = (props) => {
    const context = useContext(NetworkContext)

    useEffect(() => {
        setUpProps(props, context);
    }, [context, props])

    return (
        <div
            onClick={(e) => {
                handleEvent(e, context, props)
                props.stopPropagation && e.stopPropagation();
            }}
        >
            {props.children}
        </div>
    );
}

OnClick.propTypes = {
    /**
     * The type of the provided event.
     * When not specified the default event type is used.
     */
    type: PropTypes.string,
    /**
     * The payload to be sent.
     * It can be any object. Must be predefined in the process configuration.
     */
    payload: PropTypes.object.isRequired,
    /**
     * A callback function which triggers the send event.
     * @param: {Object} message The message ready to be sent.
     */
    onSend: PropTypes.func,
    /**
     * A boolean which stops the down propagation of the click event to children.
     * When not specified default is false.
     */
    stopPropagation: PropTypes.bool,
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
}

/**
 * The onSubmit component handles all submit events passed through its children.
 */
const OnSubmit = (props) => {
    const context = useContext(NetworkContext);

    useEffect(() => {
        setUpProps(props, context);
    }, [context, props])

    return (
        <div
            onSubmit={(e) => {
                e.preventDefault();
                let payload = {};
                let text;

                // Framework compliant utterance type
                if (props.type === "utterance") {
                    text = e.target[0].value;
                }

                // Standard OnSubmit type
                else {
                    // for each element in the form
                    for (let i = 0; i < e.target.length; i++) {
                        let t = e.target[i];
                        let label;
                        t.parentNode
                            .childNodes.forEach((childNode) => {
                                if (childNode.nodeName === 'LABEL') {
                                    label = childNode.textContent
                                }
                            }
                        );
                        /* t.parentNode should be formatted this way:
                            <div class="field">
                                <label>First Name</label>
                                <input placeholder="First Name" type="text">
                            </div>
                        */
                        let value = (t.type === "checkbox" || t.type === "radio") ? t.checked : t.value;
                        if (t.name) {
                            payload[t.name] = value;
                        } else if (label)
                        {
                            payload[label] = value;
                        } else {
                            payload[`field_${i}`] = value;
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
}

OnSubmit.propTypes = {
    /**
     * The type of the provided event.
     * When not specified the default event type is used.
     *
     * As onSubmit can be used for wrapping all kinds of forms,
     * it can be useful to specify the type "utterance" the form
     * is used just to handle input. In this case it must be provided with
     * the first child as <input type="text" />
     */
    type: PropTypes.string,
    /**
     * The payload to be sent.
     * It can be any object. Must be predefined in the process configuration.
     */
    payload: PropTypes.object.isRequired,
    /**
     * A callback function which triggers the send event.
     * @param: {Object} message The message ready to be sent.
     */
    onSend: PropTypes.func,
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
}

export default {OnClick, OnSubmit};
