from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid


class Command(BaseModel):
    text: str
    

class CommandToSend(Command):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
