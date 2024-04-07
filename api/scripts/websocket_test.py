import asyncio
import websockets
import json

async def receive_commands(target_id: str, access_key: str, server_url: str):
    uri = f"{server_url}/ws/target/{target_id}?access_key={access_key}"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                command = json.loads(message)
                print(f"Received command: {command}")
                # Process the command as needed here
                # For example, execute the command or log it
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    target_id = "2cf6271f-acfe-4bad-83e4-ecf099b6237f"
    access_key = "11e860d8-ffb2-4150-b382-f8f154372b1e"
    server_url = "ws://localhost:8000/io-target"  # Use the appropriate server URL and protocol (ws or wss for secure connections)

    asyncio.run(receive_commands(target_id, access_key, server_url))
