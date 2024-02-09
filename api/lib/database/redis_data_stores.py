import json
import redis
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional
from api.common import CommandToSend, RecieveTextResponse

class RedisCommandStore:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def store_command(self, command: CommandToSend) -> str:
        self.redis_client.set(f"command_details:{command.id}", command.model_dump_json(), ex=3600)
        return command.id

    def get_command_details(self, command_id: str) -> Optional[CommandToSend]:
        command_details = self.redis_client.get(f"command_details:{command_id}")
        if command_details:
            return CommandToSend.model_validate_json(command_details)
        return None

    def store_command_response(self, command_id: str, response: RecieveTextResponse) -> bool:
        if self.get_command_details(command_id):
            self.redis_client.set(f"command_response:{command_id}", response.model_dump_json(), ex=3600)
            return True
        return False

    def get_command_response(self, command_id: str) -> Optional[RecieveTextResponse]:
        response = self.redis_client.get(f"command_response:{command_id}")
        if response:
            return RecieveTextResponse.model_validate_json(response)
        return None
