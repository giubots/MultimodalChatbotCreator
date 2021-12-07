/**
 * Components library.
 * This file contains all wrappers to be added to the pre-existing
 * ui elements in order to add network functionalities.
 *
 * @version 1.2.0
 * @author [Davide Savoldelli](https://github.com/savdav96)
 */

import React, {useEffect, useContext} from "react";
import {NetworkContext} from './NetworkManager';
import PropTypes from "prop-types";

function handleEvent(event, context, props, payload, text) {
    if (props.disabled) {
        return;
    }
    let message = {
        type: props.type || "data",
    }
    if (props.type === "utterance") {
        message["utterance"] = text;
    } else {
        message["payload"] = {"data": props.payload || payload};
        if (props.intent) {
            message.payload = {...message.payload, intent: props.intent};
        }
    }
    props.onSend && props.onSend(message);
    console.log("[handleEvent]:", message);
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
     * Sets the intent field to be set in the payload.
     */
    intent: PropTypes.string,
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
    /**
     * Disables the activity of the OnClick
     * Default is false.
     */
    disabled: PropTypes.bool,
}

OnClick.defaultProps = {
    stopPropagation: false,
    disabled: false,
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

                        if (!props.blacklist || !props.blacklist.includes(t.type)) {
                            let value = (t.type === "checkbox" || t.type === "radio") ? t.checked : t.value;

                            switch (props.keyType) {
                                case "attribute": {
                                    payload[t[props.attributeName]] = value;
                                    break;
                                }
                                case "label": {
                                    t.parentNode
                                        .childNodes.forEach((child) => {
                                            if (child.nodeName === 'LABEL') {
                                                let label = child.textContent
                                                payload[label] = value;
                                            }
                                        }
                                    );
                                    break;
                                }
                                case "custom": {
                                    payload[`${props.customPrefix}${i}`] = value;
                                    break;
                                }
                                default: {
                                    break;
                                }
                            }
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
     * Sets the intent field to be set in the payload.
     */
    intent: PropTypes.string,
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
    /**
     * Disables the activity of the OnSubmit
     * Default is false.
     */
    disabled: PropTypes.bool,
    /**
     * Sets how to get the key name for the payload in the form.
     * It can be set to "attribute", "label" or "custom".
     */
    keyType: PropTypes.string.isRequired,
    /**
     * Sets the name of the attribute from which get the key name
     * for the payload in the form.
     * It must be set in every input elements.
     */
    attributeName: PropTypes.string,
    /**
     * Sets the prefix of the custom key name
     * for the payload in the form.
     * It must be used if keyType is set to "custom".
     */
    customPrefix: PropTypes.string,
    /**
     * Sets the attribute input types whose names are to be
     * excluded in the payload.
     */
    blacklist: PropTypes.arrayOf(PropTypes.string),
}

OnSubmit.defaultProps = {
    keyType: "attribute",
    attributeName: "name",
    customPrefix: "",
    blacklist: ["submit"],
    disabled: false,
}

// eslint-disable-next-line import/no-anonymous-default-export
export default {OnClick, OnSubmit};
