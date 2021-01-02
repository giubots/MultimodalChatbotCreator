import asyncio
import websockets
import json
import time


async def client():
    uri = "ws://localhost:8765"
    interaction = None
    uid = input("What's your name? ")
    for i in range(100):
        ws_headers = {
            'interaction': interaction,
            'uid': uid
        }
        async with websockets.connect(uri, extra_headers=ws_headers) as websocket:

            if interaction is None:
                # this is an example of an interaction,
                # such that of a user sending messages to a chatbot.
                # sometimes the connection can be closed unwillingly.
                # So the first time we open the chat interaction
                # from the client side, the interaction id is kept.
                # in this case the interaction id is the id of the first
                # successful websocket connection.
                # This interaction id is then sent to the server via the
                # headers.
                interaction = websocket.request_headers.get('Sec-WebSocket-Key')

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
            time.sleep(5)


asyncio.get_event_loop().run_until_complete(client())