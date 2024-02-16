from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid
from api.commands import Command as CommandEnum
from api.commands import ResponseType

class Command(BaseModel):
    text: CommandEnum
    command_args: dict
    
class CommandToSend(Command):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    response_type: ResponseType

class StandardResponse(BaseModel):
    command_id: str
    access_key: str
    target_id: str    

class CommandResult(BaseModel):
    result: str | list | dict
    success: bool

class RecieveTextResponse(StandardResponse):
    response: CommandResult