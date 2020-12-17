import React from "react";
import { ws } from "./index";

const handleEvent = (e, type, id, payload) => {
    e.stopPropagation();
    console.debug("Sending data...");
    /*ws.send(JSON.stringify({
        type, id, payload
    }));*/
}


export const _onClick = (props) => {
    return(
        <div onClickCapture={(e) => handleEvent(e,"click", props.id, props.payload)}>
            {props.children}
        </div>
    );
}

export const _onScroll = (props) => {
    return (
        <>
            {props.children}
        </>
    );
}

export const _onFocus = (props) => {
    return (
        <>
            <p>Scrollable</p>
            {props.children}
        </>
    );
}
