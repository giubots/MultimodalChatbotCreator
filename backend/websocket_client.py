import asyncio
import websockets
import json


# async def hello():
#     uri = "ws://localhost:8765"
#     async with websockets.connect(uri) as websocket:
#         name = input("What's your name? ")
#
#         await websocket.send(name)
#         print(f"> {name}")
#
#         greeting = await websocket.recv()
#         print(f"< {greeting}")
#
#
# asyncio.get_event_loop().run_until_complete(hello())

async def client():
    uri = "ws://localhost:8765"
    ws_headers = {
        # interaction is None when you are starting it,
        # then you need to set it to the initial websocket key value
        # to continue the interaction.
        'interaction': None,
        # the user id identifies the user in the backend and is required
        'uid': 'user id'
    }
    async with websockets.connect(uri, extra_headers=ws_headers) as websocket:
        # this is the websocket key value you need to provide
        # if you want to start a new websocket connection for the
        # same interaction.
        # if the interaction is set to None, a new interaction will be
        # created. (and a new Framework process instantiated)
        # see websocket_client_interrupted.py for more information
        ws_key = websocket.request_headers.get('Sec-WebSocket-Key')

        event_utterance = {
            'type': 'utterance',
            'utterance': 'my_utterance'  # this is an example text
        }

        event_data = {
            'type': 'data',
            'payload': {
                'echo': 'Bob'  # this is an example data
            }
        }

        # switch between test utterance or data
        event = event_data

        await websocket.send(json.dumps(event))
        print(f"> {event}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(client())
