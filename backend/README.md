
[comment]: <> (TODO: Rasa)

# MULTIMODAL CHATBOT CREATOR - BACKEND

This backend interfaces with the framework and the frontend.

It contains all the logic to make it all work, and it needs to be implemented in your server.

___

# Set up the server

### 1. Install the framework

To install the framework, use this github command on your terminal:

```shell
pip install 'git+https://github.com/giubots/MultimodalChatbotCreator@feature-nlu#egg=mccreator-framework&subdirectory=framework'
```

### 2. Initialize the backend

The backend must contain your configuration files. They represent how your website works, and the flow of operations that you want the user to follow.

For some examples of the configuration files, look at the Quickstart below.

# Quickstart

For the Quickstart guide, click on
[this link](examples/README.md)

# How it works

The server communicates via websockets or the rest api (whichever you prefer).

The example frontend is written in React and implements the websockets. When the server receives a websocket connection request, it creates an instance of the framework for that user and that interaction. In the future it will be possible to keep some user info and tap into that data to better respond to the customer (the more data we have about the customer, the better we can help him reach his goals easily).

### Connection

The server asks for an identification (at the moment it's just a user id `uid`, but it could be integrated into your website's authentication system). 

If it doesn't receive an `interaction` (at the time of websocket connection), it uses the websocket key to generate the interaction id, and sends it back to the client.

Then the interaction can start. The server usually sends the welcome message of the framework to the client, such as "Welcome user, how old are you?"

### Interaction

The frontend must send either text or data.

If it sends text, then the json transmitted should be as follows:
```json
{
  "type": "utterance",
  "utterance": "my_utterance"
}
```
Where `my_utterance` is the text the client wants to send to the server (for example a message the user wrote in the chat).

If it instead sends data (such as when the user has performed a certain action on your page, or has clicked on a specific button), this is what you should send to the server:
```json
{
  "type": "data",
  "payload": {
    "my_activity": "my_data"
  }
}
```
This sends the data `my_data` to the activity `my_activity` of the process defined by you in `config/my_process.json`.

### Close connection
When it is time to close the connection, simply disconnect the websocket.

If you want to resume the process at a later time, just memorize the interaction id and send it as a parameter when you connect to a new websocket: this way the interaction will resume from the same point you left it before!