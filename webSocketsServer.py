import asyncio
import websockets
import subprocess

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print(f"a client is connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"message received: {message}")
            await websocket.send("Compiling IAR...")

            try:
                if message == "IAR Compile":
                    result = subprocess.run(["python", "autoKeil.py"], check=True)
                else:
                    result = subprocess.run(["python", "autoKeil.py", message], check=True)
                
                if result.returncode == 0:
                    await websocket.send("Compiling IAR success.")
            except subprocess.CalledProcessError as e:
                await websocket.send(f"error code {e.returncode}")
            except Exception as e:
                await websocket.send(str(e))

            for client in connected_clients:
                if client != websocket:
                    await client.send(f"received: {message}")
    except websockets.ConnectionClosed:
        print("a client is disconnected")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server running on ws://0.0.0.0:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
