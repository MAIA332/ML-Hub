import asyncio
from websockets.server import serve
import json

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
        
        if('{' not in message):
            await websocket.send(message)
        else:
            request = json.loads(message)
                
            await websocket.send(json.dumps(request))

async def main():
    print("Server is activated on ws://{}:{}".format(ipaddress,port))
    #async with serve(echo, "localhost", 8765):
    async with serve(echo, "0.0.0.0", port):
        await asyncio.Future() 

asyncio.run(main())