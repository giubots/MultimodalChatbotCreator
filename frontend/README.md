# react-mmcc
A Multi Modal Chatbot Creator adapter for React

[![NPM](https://img.shields.io/npm/v/react-chatbot-ui.svg)](https://www.npmjs.com/package/react-chatbot-ui) [![JavaScript Style Guide](https://img.shields.io/badge/code_style-standard-brightgreen.svg)](https://standardjs.com)

This package adds a layer of connection for process-based chatbot frameworks.
It allows to decouple the frontend ui rendering from the connection management handled by WebSocket or REST API.
It is almost completely compatible with former web applications without too much integration effort.

To work with it, you need to set up a backend chatbot service before. More information [here](../../backend/README.md).

## Install

```bash
npm install --save react-mmcc
```

## Usage

Firstly, you need to wrap your all your application components that need a network connection layer with the `NetworkManager` component.
```jsx
import React from 'react'

import {NetworkManager, Components} from "react-chatbot-ui";

const App = () => {
    return (
        <NetworkManager url={"ws://YOUR_WS_URL:YOUR_WS_PORT"} uid={"YOUR_UID"}>
            ...
        </NetworkManager>
    );
}
```

Then, you can wrap your components with the event catchers in the `Components` class.

```jsx
const App = () => {
    return (
        <NetworkManager url={"ws://YOUR_WS_URL:YOUR_WS_PORT"} uid={"YOUR_UID"}>

            <Components.OnClick>
                <button>My button</button>
            </Components.OnClick>

            <Components.OnSubmit>
                <form>
                    <input type={"text"} name={"email"} />
                    <input type={"password"} name={"password"} />
                    <input type={"submit"} />
                </form>
            </Components.OnSubmit>

        </NetworkManager>
    );
}
```
## Components

### `NetworkManager`
It is used to manage the connection with the backend service and handle the callbacks.

#### Props

| Prop | Type | Default | Note |
| --- | --- | --- | --- |
| `url` | `String` | `undefined` | (Required) The url of the connection. It supports WebSocket protocol. In future it will handle HTTP connections with REST API. |
| `uid` | `String` | `undefined` | (Required) The unique identifier of the connection Must be pre-shared before connecting. |
| `useRest` | `boolean` | `false` | Not implemented yet. |

#### Events
| Event | Returns  | Note |
| --- | ---  | --- |
| `onMessage` | `string` | A callback function which triggers the receive event. This is used to handle the received messages |
| `onOpen` | `Event` | A callback function which triggers the open event. |
| `onClose` | `Event` | A callback function which triggers the close event. |
| `onError` | `Event` | A callback function which triggers the error event. |

### `Components.OnClick`
The onClick component handles all click events passed through its children.

#### Props

| Prop | Type | Default | Note |
| --- | --- | --- | --- |
| `type` | `String` | `event.type` | The type of the provided event. |
| `payload` | `Object` | `{}` | The payload to be sent. It can be any object. Must be predefined in the process configuration. |
| `stopPropagation` | `boolean` | `false` | A boolean which stops the down propagation of the click event to children. |
| `disabled` | `boolean` | `false` | A boolean which disables the activity of the OnClick. |

#### Events
| Event | Returns  | Note |
| --- | ---  | --- |
| `onMessage` | `string` | A callback function which triggers the receive event. This is used to handle the received messages |
| `onOpen` | `Event` | A callback function which triggers the open event. |
| `onClose` | `Event` | A callback function which triggers the close event. |
| `onError` | `Event` | A callback function which triggers the error event. |
| `onSend` | `string` | A callback function which triggers the sending event. This is used to handle the messages about to be sent |

### `Components.OnSubmit`
The onClick component handles all click events passed through its children.

#### Props

| Prop | Type | Default | Note |
| --- | --- | --- | --- |
| `type` | `String` | `event.type` | The type of the provided event. As onSubmit can be used for wrapping all kinds of forms, it can be useful to specify the type "utterance" the form is used just to handle input. In this case it must be provided with the first child as `<input type="text" />` |
| `payload` | `Object` | `{}` | The payload to be sent. It can be any object. Must be predefined in the process configuration. |
| `disabled` | `boolean` | `false` | A boolean which disables the activity of the OnSubmit. |

#### Events
| Event | Returns  | Note |
| --- | ---  | --- |
| `onMessage` | `string` | A callback function which triggers the receive event. This is used to handle the received messages |
| `onOpen` | `Event` | A callback function which triggers the open event. |
| `onClose` | `Event` | A callback function which triggers the close event. |
| `onError` | `Event` | A callback function which triggers the error event. |
| `onSend` | `string` | A callback function which triggers the sending event. This is used to handle the messages about to be sent |


## License

MIT © [savdav96](https://github.com/savdav96)
