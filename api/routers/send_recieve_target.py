import datetime
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from fastapi.security import APIKeyQuery
from ..globals import redis_client_aio, target_db_manager, target_status_manager
from ..config import MAX_COMMAND_LIFE
from .common import CommandToSend

router = APIRouter()



@router.websocket("/ws/target/{target_id}")
async def websocket_endpoint(websocket: WebSocket, target_id: str, access_key: str = APIKeyQuery(name="access_key")):
    target = target_db_manager.get_target_by_id(target_id)
    if not target or target.target_access_key != access_key:
        await websocket.close(code=1008)
        return
    
    await websocket.accept()
    target_status_manager.mark_target_online(target_id=target_id)
    print(f"Accepted the connection for target {target_id}.")
    pubsub = redis_client_aio.pubsub()
    await pubsub.subscribe(target_id)

    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                command = CommandToSend.model_validate_json(message['data'])
                print(f"Sending command {command} to {target_id}")
                if (datetime.datetime.now(datetime.timezone.utc) - command.timestamp).total_seconds() > MAX_COMMAND_LIFE:
                    continue
                await websocket.send_text(command.model_dump_json())
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for target {target_id}.")
    finally:
        target_status_manager.mark_target_offline(target_id) 
        await pubsub.unsubscribe(target_id)
