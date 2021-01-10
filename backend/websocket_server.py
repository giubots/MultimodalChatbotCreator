import asyncio
import websockets
import json
from functions import *


async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

    # await  websockets.
    # function when on open: framework
    # create Framework(Process(['start', 'end'])...
    # on websocket.recv
    # differenza tra messaggio che contiene stringa e dati
    # se c'e un utterance
    # type utterance
    # my_recv = {
    #     "type": "utterance", ['utterance', 'data']
    #     "utterance": "my utterance", # my_framework.handle_text_input(my_input["utterance"])
    #     "payload": {...}             # my_framework.handle_data_input({...})
    # }

    # utterance e' frase, quindi chiamo handle text input
    # altrimenti chiamo handle data input
    # salvo il risultato e lo invio alla socket

my_framework = dict()

connected = set()


async def handler(websocket: websockets.WebSocketServerProtocol, path):
    # Register
    connected.add(websocket)
    print(connected)
    # this is the session key that we are going to use to
    # set up the interaction. we are going to use the first one
    # received by the server to identify it
    ws_key = websocket.request_headers.get('Sec-WebSocket-Key')
    # these are the query parameters: interaction and uid:
    params = get_params(path)
    # this will be the interaction id received by the client,
    # and will correspond to the first websocket request for this
    # interaction.
    # [the setdefault function works to get the value from dict,
    # and if the value is not present, get the default value None
    # instead of raising a keyError and shutting down the server
    i = params.setdefault('interaction', None)
    # this is the user id and is used to keep track of different users
    uid = params.setdefault('uid', None)
    if uid == 'None' or uid is None:
        if i == 'None' or i is None:
            # it means that the client is initializing and asking
            # for the uid
            await websocket.send(uuid_generator())
            return

        error = {'error': 'Insert the uid (user id) in the headers'
                          ' and try again.'
                          ' Tip: try to send an empty request,'
                          ' and you will receive a server-generated'
                          ' uid!'}
        print(error)
        await websocket.send(json.dumps(error))
        return
    elif uid not in my_framework:
        my_framework[uid] = dict()

    if i == 'None' or i is None:
        # this is when the client starts the interaction
        i = ws_key
        # create framework
        my_framework[uid][i] = create_framework()
        # send the interaction id (the websocket key) to client
        await websocket.send(i)
        # init framework
        welcome_message = welcome_message_framework(my_framework[uid][i])
        await websocket.send(json.dumps(welcome_message))
    print(my_framework)
    try:
        async for message in websocket:
            print(message)
            print()  # for better visual distinction between messages
            recv = json.loads(message)
            if recv['type'] == 'utterance':
                send = my_framework[uid][i].handle_text_input(recv['utterance'])
                await websocket.send(json.dumps(send))
            else:
                send = my_framework[uid][i].handle_data_input(recv['payload'])
                await websocket.send(json.dumps(send))
    finally:
        connected.remove(websocket)


if __name__ == '__main__':
    # start_server = websockets.serve(hello, "localhost", 8765)
    start_server = websockets.serve(handler, "", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
