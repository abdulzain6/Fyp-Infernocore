import asyncio
import time
import httpx
import websockets
import uuid

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from enum import Enum

from dependencies.modules.commands import Command as CommandEnum, CommandResult
from dependencies.modules.commands import CommandArgs
from dependencies.globals import command_executor

class ResponseType(Enum):
    FILE_RESPONSE = "FILE_RESPONSE"
    STREAM = "STREAM"
    JSON_RESPONSE = "JSON_RESPONSE"
    
class Command(BaseModel):
    text: CommandEnum
    command_args: CommandArgs
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    response_type: ResponseType
    
class RecieveTextResponse(BaseModel):
    command_id: str
    response: CommandResult
    access_key: str
    target_id: str   


class WebSocketClient:
    def __init__(self, base_url: str, target_id: str, access_key: str):
        self.base_url = base_url
        self.target_id = target_id
        self.access_key = access_key
        self.websocket_url = f"ws://{base_url}/io-target/ws/target/{target_id}?access_key={access_key}"
        self.response_url = f"http://{base_url}/io-target/commands/response"
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.command_queue = asyncio.Queue()

    async def connect_websocket(self):
        while True:
            try:
                async with websockets.connect(self.websocket_url) as websocket:
                    print("Successfully connected")
                    await self.handle_messages(websocket)
            except websockets.ConnectionClosed:
                print("WebSocket connection closed, attempting to reconnect...")
            except Exception as e:
                print(f"WebSocket connection failed: {e}, retrying in 5 seconds...")
            await asyncio.sleep(5)  # Delay before attempting to reconnect

    async def handle_messages(self, websocket):
        receive_task = asyncio.create_task(self.receive_commands(websocket))
        execute_task = asyncio.create_task(self.execute_commands())
        done, pending = await asyncio.wait(
            [receive_task, execute_task], 
            return_when=asyncio.FIRST_COMPLETED
        )

        for task in pending:
            task.cancel()  # Cancel any pending tasks if one completes

    async def receive_commands(self, websocket):
        try:
            while True:
                message = await websocket.recv()
                try:
                    print(f"Message: {message}")
                    command = Command.model_validate_json(message)
                    await self.command_queue.put(command)
                except Exception as e:
                    print(f"Invalid command {message} {e}")
        except websockets.ConnectionClosed:
            print("WebSocket connection closed, attempting to reconnect...")
        
    async def execute_commands(self):
        while True:
            command = await self.command_queue.get()
            asyncio.create_task(self.execute_command(command))

    async def execute_command(self, command: Command):
        print(f"Executing: {command}")
        loop = asyncio.get_running_loop()
        if command.response_type == ResponseType.JSON_RESPONSE:
            response = await loop.run_in_executor(
                self.executor, self.executor_function, command
            )
            await self.send_text_response(
                RecieveTextResponse(
                    command_id=command.id,
                    response=response,
                    target_id=self.target_id,
                    access_key=self.access_key
                )
            )
        elif command.response_type == ResponseType.STREAM:
            await self.handle_stream_response(command)

    def executor_function(self, command: Command) -> CommandResult:
        print(f"Executing command: {command}")
        return command_executor(command.text, args=command.command_args) 

    async def send_text_response(self, response_in: RecieveTextResponse):
        retries = 3
        delay = 2  # Delay in seconds between retries

        async with httpx.AsyncClient() as client:
            for attempt in range(retries):
                try:
                    response = await client.post(
                        self.response_url,
                        json=response_in.model_dump(),
                        follow_redirects=True
                    )
                    response.raise_for_status()  # Raises exception for 4XX/5XX responses
                    break  # Exit the loop on success
                except httpx.HTTPStatusError as e:
                    print(f"Request failed with status code {e.response.status_code}: {e}")
                except httpx.RequestError as e:
                    print(f"Request failed with error: {e}")
                if attempt < retries - 1:  # Don't sleep after the last attempt
                    await asyncio.sleep(delay)
                    delay *= 2  # Optional: Exponential backoff

    async def handle_stream_response(self, command: Command):
        stream_ws_url = f"ws://{self.base_url}/io-target/ws/stream/response?command_id={command.id}&target_id={self.target_id}&access_key={self.access_key}"
        try:
            async with websockets.connect(stream_ws_url) as ws:
                now = time.time()
                while True:
                    # Check if the WebSocket is still open
                    if ws.open:
                        await ws.send(b'I')
                        time.sleep(1)
                        if time.time() - now > 100:
                            break
                    else:
                        print("WebSocket connection is closed.")
                        break
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"WebSocket connection was closed unexpectedly: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Any cleanup can go here
            print("Stream response handler completed.")
            
async def main():
    target_id = "2cf6271f-acfe-4bad-83e4-ecf099b6237f"
    access_key = "11e860d8-ffb2-4150-b382-f8f154372b1e"
    client = WebSocketClient("localhost:8000", target_id, access_key)
    await client.connect_websocket()

if __name__ == "__main__":
    asyncio.run(main())
