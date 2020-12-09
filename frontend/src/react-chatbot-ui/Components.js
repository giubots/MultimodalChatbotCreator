import React from "react";

export const _clickable = (props) => {
    return(
        <div
            onClick={(e) => {
                (props.onClick)();
                e.stopImmediatePropagation();
            }}
        >
            <p>Clickable</p>
            {props.children}
        </div>
    );
}

export const _scrollable = (props) => {
    return (
        <>
            <p>Scrollable</p>
            {props.children}
        </>
    );
}

