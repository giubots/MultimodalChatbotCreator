/**
 * Components library.
 * This file contains all wrappers to be added to the pre-existing
 * ui elements in order to add network functionalities.
 *
 * @version 1.0.1
 * @author [Davide Savoldelli](https://github.com/savdav96)
 */

import React from "react";
import {NetworkContext} from './NetworkManager';
import PropTypes from "prop-types";

function handleEvent(event, context, props, payload, text) {
    let message = {
        type: props.type || event.type,
    }
    if (props.type === "utterance") {
        message["utterance"] = text;
    } else {
        message["payload"] = payload || props.payload;
    }
    props.onSend && props.onSend(message);
    context.send(JSON.stringify(message));
}

/**
 * The onClick component handles all click events passed through its children.
 */
const onClick = (props) => {
    return (
        <NetworkContext.Consumer>
            {(context) => {
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
            }}
        </NetworkContext.Consumer>
    );
}

onClick.propTypes = {
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
}

/**
 * The onSubmit component handles all submit events passed through its children.
 */
const onSubmit = (props) => {
    return (
        <NetworkContext.Consumer>
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
        </NetworkContext.Consumer>
    );
}

onSubmit.propTypes = {
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
}

export default {
    onClick, onSubmit
};
