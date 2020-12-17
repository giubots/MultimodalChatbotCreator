export const ws = new WebSocket("ws://localhost:8765");
let received = [];

ws.onopen = function (event) {
    console.debug("Connection open");
}

ws.onopen = function (event) {
    console.debug("Connection open");
}

ws.onmessage = function (event) {
    console.debug("Received:", event);
    received.push(event);
    return false;
}

ws.onclose = function (event) {
    console.debug("Connection close");
    ws.close();
}

ws.onerror = function (event) {
    console.error("Error", event);
}

export const _receive = () => {
    return received.pop();
}


