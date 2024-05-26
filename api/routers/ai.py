from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from api.auth import get_user_id, security
from pydantic import BaseModel

from api.lib.ai import CommandExecutor, make_tools, make_shell_tool, commands_to_args_list, RedTeamingAI
from api.lib.database.target import TargetDBManager
from langchain_openai import ChatOpenAI
from ..globals import BASE_URL, target_db_manager, target_status_manager

class ChatInput(BaseModel):
    target_id: str
    prompt: str
    chat_history: list[tuple[str, str]] = None

router = APIRouter()

def get_online_accessible_targets(uid: str):
    accessible_targets = target_db_manager.get_targets_accessible_by_user(uid)
    accessible_target_ids = {str(target.target_id) for target in accessible_targets}
    online_target_ids = set(target_status_manager.get_online_targets())
    online_accessible_target_ids = accessible_target_ids.intersection(online_target_ids)
    return online_accessible_target_ids
   

@router.post("/chat")
def chat(
    chat_input: ChatInput,
    user_id = Depends(get_user_id),
    credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    if chat_input.target_id not in get_online_accessible_targets(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to access this target/ Target Offline")
    
    command_exec = CommandExecutor(
        auth_token=credentials.credentials,
        target_id=chat_input.target_id,
        send_command_url=f"http://{BASE_URL}/io-attacker/submit-command",
        response_url=f"http://{BASE_URL}/io-attacker/response"
    )
    tools = make_tools(
        commands_to_args_list,
        command_exec
    )
    shell_tool = make_shell_tool(command_exec)
    
    ai = RedTeamingAI(
        ChatOpenAI(),
        tools=[shell_tool, *tools]
    )
    return ai.run_agent(
        prompt=chat_input.prompt,
        chat_history=chat_input.chat_history
    )