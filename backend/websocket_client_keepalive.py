import asyncio
import websockets
import json
import time


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
    for i in range(100):
        async with websockets.connect(uri) as websocket:
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
