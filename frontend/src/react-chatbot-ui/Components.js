import React from "react";

export const _clickable = (props) => {
    const handleClick = e => {
        e.stopPropagation();
        //props.onClick();
        alert("Send data");
    }

    return(
        <div onClickCapture={handleClick}>
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

