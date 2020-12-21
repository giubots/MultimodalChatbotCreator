import asyncio
import websockets

# import framework
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'framework'))
from framework import Framework

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
    # my_recv = {​​
    #     "type": "utterance", ['utterance', 'data']
    #     "utterance": "my utterance", # my_framework.handle_text_input(my_input["utterance"])
    #     "payload": {​​...}​​             # my_framework.handle_data_input({​​...}​​)
    # }​​

    # utterance e' frase, quindi chiamo handle text input
    # altrimenti chiamo handle data input
    # salvo il risultato e lo invio alla socket



start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
