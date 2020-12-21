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
    async with websockets.connect(uri) as websocket:
        event = {
            'type': 'utterance',
            'utterance': 'my_utterance',
            'payload': 'ok'
        }

        await websocket.send(json.dumps(event))
        print(f"> {event}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(client())