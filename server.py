import asyncio
from websockets.server import serve
import json
from commons.models import Utils
from commons.data import Files, Modeling
from commons.models import RandomForest
import pickle
import pandas as pd


def getIpAddress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipaddress = s.getsockname()[0]
    s.close()
    return ipaddress

ipaddress = getIpAddress()
port = 8765

async def echo(websocket):
    print(f"New connection from {websocket.remote_address}")

    async for message in websocket:
        print("received from {}:{} : ".format(websocket.remote_address[0],websocket.remote_address[1]) + message)
        
        if '{' not in message:
            await websocket.send(message)
        else:
            request = json.loads(message) # Recebe uma mensagem em json

            response = await process_message(request)

            await websocket.send(response) # Retorna o objeto direto

async def process_message(message):
    
    type_ = message["type"]
    args = [message[i] for i in list(message.keys()) if i != "type"]

    def load_model(args):
        MyModel = Utils("", "load", args)
        return MyModel
    
    def load_file(args):
        fileManipulation = Files(args[0], args[1])  # ["Datassets/tested.csv", "Datassets/titanic.json", "PassengerId"]
        
        return fileManipulation
    
    def pre_processing(args):
        MyModeling = Modeling(args[0], args[1], drops=args[2])  # ["Cabin", "Name", "Embarked", "Ticket", "PassengerId"]
        
        return MyModeling
    
    def create_model(args):
        models_map = {
            "random-forest": RandomForest
        }

        MyModel = models_map[args[0]](pd.DataFrame(args[1]["X_train"]), pd.DataFrame(args[1]["y_train"]), pd.DataFrame(args[1]["X_test"]), pd.DataFrame(args[1]["y_test"]))
        return MyModel
    
    key_map = {
        "load-model": load_model,
        "file": load_file,
        "pre-processing": pre_processing,
        "create-model": create_model
    }
    
    obj_instance = key_map[type_](args)
    return pickle.dumps(obj_instance)

async def main():
    print("Server is activated on ws://{}:{}".format(ipaddress, port))
    async with serve(echo, "0.0.0.0", port,ping_interval=120, ping_timeout=120):
        await asyncio.Future()

asyncio.run(main())
