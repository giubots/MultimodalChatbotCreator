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

import {NetworkManager, Components} from "react-mmcc";

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
| `intent` | `string` | `undefined` | Sets the intent field to be set in the payload. |
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
| `intent` | `string` | `undefined` | Sets the intent field to be set in the payload. |
| `disabled` | `boolean` | `false` | A boolean which disables the activity of the OnSubmit. |
| `keyType` | `"attribute"` &#124; `"label"` &#124; `"custom"`  | `"attribute"` | Sets how to get the key name for the payload in the form. |
| `attributeName` | `string` | `"name"` | Sets the name of the attribute from which get the key name for the payload in the form |
| `customPrefix` | `string` | `""` | Sets the prefix of the custom key name for the payload in the form. |
| `blacklist` | `array` | `["submit"]` | Sets the attribute input types whose names are to be excluded in the payload. |


#### Events
| Event | Returns  | Note |
| --- | ---  | --- |
| `onMessage` | `string` | A callback function which triggers the receive event. This is used to handle the received messages |
| `onOpen` | `Event` | A callback function which triggers the open event. |
| `onClose` | `Event` | A callback function which triggers the close event. |
| `onError` | `Event` | A callback function which triggers the error event. |
| `onSend` | `string` | A callback function which triggers the sending event. This is used to handle the messages about to be sent |

## General notes:

### `NetworkManager`

The connection must necessarily be set up in advance before trying to send messages.
In fact, an `uid` (the string which allows the persistence of session) must be shared in a handshake before the chatbot connection.
To do this, using `localStorage` or `sessionStorage` is recommended.

### `Components.OnSubmit`

#### `keyType` selection
When using `OnSubmit` in a standard form component (the one carrying no utterance), the props `keyType` must be carefully chosen in order to automatically 
compose a suitable payload for the chatbot backend. 

If you need to pick the key of the payload values from the `<label />` associated with the `<input />` component, you are forced 
to enclose the `form` elements within a specific hierarchy: there must be a parent which wraps only an input and its associated label, in the following way.

```html
<form>
    <fieldset>
        <div>
            <label>My awesome label</label>
            <input type="text" />
        </div>
        <div>
            <label>My other awesome label</label>
            <input type="text" />
        </div>
    </fieldset>
</form>
```

#### Utterance handling
When using `OnSubmit` as an utterance forwarder, you are intending to keep the user input and to send it to the NLU backend for further processing.
To signal this, the prop `type` must be set to `"utterance"`. Again, you are forced to compose the form children in a specific way. 
Indeed, the input component must be the first child in the form.

```html
<form>
    <input type="text">
    <input type="submit">
</form>
```

## License

GPL v3 © [savdav96](https://github.com/savdav96)
