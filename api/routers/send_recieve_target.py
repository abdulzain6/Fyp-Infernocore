from asyncio import CancelledError, create_task
import datetime
from fastapi import HTTPException, WebSocket, APIRouter, WebSocketDisconnect
from fastapi.security import APIKeyQuery
from ..globals import redis_client_aio, target_db_manager, target_status_manager, command_store
from ..config import MAX_COMMAND_LIFE
from api.common import CommandToSend, RecieveTextResponse


router = APIRouter()


async def listen_for_commands(pubsub, websocket, target_id):
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                command = CommandToSend.model_validate_json(message['data'])
                print(f"Sending command {command} to {target_id}")
                if (datetime.datetime.now(datetime.timezone.utc) - command.timestamp).total_seconds() > MAX_COMMAND_LIFE:
                    continue  # Skip old commands
                await websocket.send_text(command.model_dump_json())
    except CancelledError:
        pass
    except Exception as e:
        print(f"Error processing messages: {e}")

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

    listen_task = create_task(listen_for_commands(pubsub, websocket, target_id))

    try:
        # Wait for the client to disconnect
        await websocket.receive_text()
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for target {target_id}.")
    finally:
        listen_task.cancel()  # Cancel the listening task when the client disconnects
        await pubsub.unsubscribe(target_id)
        target_status_manager.mark_target_offline(target_id)
        print("Cleaned up after disconnection.")

        # Ensure the cancellation is processed
        try:
            await listen_task
        except CancelledError:
            print("Listen task cancelled.")


@router.post("/commands/response")
def receive_command_response(response: RecieveTextResponse):
    target = target_db_manager.get_target_by_id(response.target_id)
    if not target or target.target_access_key != response.access_key:
        raise HTTPException(status_code=400, detail="Target not found/ Invalid key")
    
    try:
        if command_store.store_command_response(response.command_id, response):
            return {"status": "success", "message": "Response received"}
        else:
            raise HTTPException(status_code=400, detail="Invalid command ID or command expired")
    except Exception as e:
        print(F"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid response format")
    
    
    
@router.websocket("/ws/stream/response")
async def recieve_stream_response(websocket: WebSocket, command_id: str, access_key: str, target_id: str):
    target = target_db_manager.get_target_by_id(target_id)
    if not target or target.target_access_key != access_key:
        raise HTTPException(status_code=400, detail="Target not found/ Invalid key")
    
    await websocket.accept()
    print(f"Publishing to stream:{command_id}")
    try:
        while True:
            data = await websocket.receive_bytes()
            await redis_client_aio.publish(f"stream:{command_id}", data)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for client {command_id}")

