import requests
import time

# Base URL of your endpoint
BASE_URL = "http://localhost:8000/io-attacker"

# Your API token
API_TOKEN = input("Enter token:")

headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
}

def send_command(command_text, command_args={}):
    json_data = {
        'text': command_text,
        'command_args': command_args,
    }
    response = requests.post(
        f'{BASE_URL}/submit-command/2cf6271f-acfe-4bad-83e4-ecf099b6237f',
        headers=headers,
        json=json_data,
    )
    if response.status_code == 200:
        return response.json()["command"]["id"]
    else:
        print("Failed to submit command")
        return None

def get_command_response(command_id):
    response = requests.get(
        f'{BASE_URL}/response/{command_id}',
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get command response")
        return None

import json
while True:
    command_text = input("Enter command (or type 'exit' to quit): ")
    command_args = input("Enter command args: ")
    command_args = json.loads(command_args)
    if command_text == "exit":
        break
    command_id = send_command(command_text, command_args)
    if command_id:
        print(f"Command ID: {command_id}")
        # Polling for response
        while True:
            result = get_command_response(command_id)
            if result:
                print(result)
                break
            else:
                print("Waiting for command response...")
                time.sleep(2)  # Wait before polling again
