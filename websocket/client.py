import asyncio
from websockets.sync.client import connect
import json

jsondata = {"type": "setParam", "param1": 30, "param2": 2.3}

def hello():
    with connect("ws://192.168.0.15:8765") as websocket:

        while True:
            
            websocket.send(json.dumps(jsondata)) #
            message = websocket.recv()
            print(f"Received from server : {message}")

hello()