from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from ..auth import get_current_user
from ..globals import target_db_manager, redis_client
from .common import Command, CommandToSend

router = APIRouter()


@router.post("/submit-command/{target_id}")
def submit_command(target_id: str, command: Command, current_user=Depends(get_current_user)):
    target = target_db_manager.get_target_by_id(target_id)
    if not target or current_user["user_id"] not in target.accessible_by_users:
        raise HTTPException(status_code=403, detail="Not authorized to access this target")

    command_to_send = CommandToSend(**command.model_dump(), timestamp=datetime.now(timezone.utc))
    redis_client.publish(target_id, command_to_send.model_dump_json())
    return {"command": command_to_send, "message": "Command submitted successfully"}
