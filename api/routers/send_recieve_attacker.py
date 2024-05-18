import asyncio
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from ..auth import get_user_id, get_set_user_id
from ..globals import target_db_manager, redis_client, command_store, redis_client_aio
from api.common import Command, CommandToSend
from api.commands import command_response_map

router = APIRouter()


@router.post("/submit-command/{target_id}")
def submit_command(target_id: str, command: Command, uid=Depends(get_user_id)):
    target = target_db_manager.get_target_by_id(target_id)
    if not target or uid not in target.accessible_by_users:
        raise HTTPException(status_code=403, detail="Not authorized to access this target")

    command_to_send = CommandToSend(**command.model_dump(), timestamp=datetime.now(timezone.utc), response_type=command_response_map[command.text])
    command_store.store_command(command=command_to_send)
    redis_client.publish(target_id, command_to_send.model_dump_json())
    return {"command": command_to_send,"message": "Command submitted successfully"}

@router.get("/response/available/{command_id}")
def check_response_availability(command_id: str, user_id = Depends(get_user_id)):
    response = command_store.get_command_response(command_id)
    if response:
        target = target_db_manager.get_target_by_id(response.target_id)
        if not target or user_id not in target.accessible_by_users:
            raise HTTPException(status_code=403, detail="Not authorized to access this target")
        
    return {"status": "success", "available": bool(response)}

@router.get("/response/{command_id}")
def get_command_response(command_id: str, user_id = Depends(get_user_id)):
    response = command_store.get_command_response(command_id)
    if response:
        target = target_db_manager.get_target_by_id(response.target_id)
        if not target or user_id not in target.accessible_by_users:
            raise HTTPException(status_code=403, detail="Not authorized to access this target")
        
        print(response)
        return response.response
    else:
        raise HTTPException(status_code=404, detail="Response not found")

@router.websocket("/ws/listen")
async def websocket_listen(websocket: WebSocket, target_id: str, command_id: str, auth_token: str):
    try:
        user_id = get_set_user_id(auth_token)  # Assuming this function correctly sets/gets the user ID
    except Exception:
        print("Bad token")
        await websocket.close(code=1008)  # Use appropriate WebSocket close code
        raise HTTPException(status_code=403, detail="Not authorized to access this target")
            
    target = target_db_manager.get_target_by_id(target_id)
    if not target or user_id not in target.accessible_by_users:
        await websocket.close(code=1008)  # Use appropriate WebSocket close code
        print("Bad target")
        raise HTTPException(status_code=403, detail="Not authorized to access this target")
    
    await websocket.accept()
    channel_name = f"stream:{command_id}"
    pubsub = redis_client_aio.pubsub()
    await pubsub.subscribe(channel_name)

    try:
        while True:
            message = await pubsub.get_message(timeout=15)
            if message is None:
                print("Timeout reached, closing WebSocket")
                await websocket.close()
                break
            if message and message['type'] == 'message':
                await websocket.send_bytes(message['data'])
    except WebSocketDisconnect: 
        print(f"WebSocket disconnected for listener {target_id}")
    finally:
        await pubsub.unsubscribe(channel_name)
        print("Unsubscribed and cleaned up")