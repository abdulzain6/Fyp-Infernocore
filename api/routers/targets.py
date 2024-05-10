from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
from ..auth import get_current_user
from ..globals import target_db_manager, user_db_manager, target_status_manager, file_manager, BASE_URL, CLIENT_FOLDER
from api.lib.database import TargetModel
from pydantic import BaseModel

import logging
import io
import uuid
import shutil
import subprocess
import tempfile
import os
import json
import base64

router = APIRouter()

class TargetResponse(BaseModel):
    status: str
    error: Optional[str] = None
    target: Optional[TargetModel] = None

class DeleteTargetResponse(BaseModel):
    status: str
    error: Optional[str] = None
    target_id: Optional[str] = None

class TargetModelInput(BaseModel):
    accessible_by_users: List[str] 
    name: str
    icon_base64: str | None = None


def user_can_access_target(user_id: str, target_id: str) -> bool:
    return target_db_manager.is_target_accessible_by_user(target_id, user_id)



class Config(BaseModel):
    TARGET_ID: str
    ACCESS_KEY: str
    icon: Optional[str] = None  # Base64 encoded icon file, now optional


def create_executable(config: Config):
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()

        # Set up paths for folder copy
        print("Client:", CLIENT_FOLDER)
        destination_folder = os.path.join(temp_dir, "client")
        print("Dest:", destination_folder)
        shutil.copytree(CLIENT_FOLDER, destination_folder)

    
        # Prepare PyInstaller command
        client_py = os.path.join(destination_folder, "client.py")
        with open(client_py, "r") as fp:
            client_py_data = fp.read()
            client_py_data = client_py_data.replace("TARGETID_TO_REPLACE", config.TARGET_ID)
            client_py_data = client_py_data.replace("ACCESS_KEY_TO_REPLACE", config.ACCESS_KEY)
            client_py_data = client_py_data.replace("BASE_URL_TO_REPLACE", BASE_URL)

        with open(client_py, "w") as fp:
            fp.write(client_py_data)


        print("Running pyinstaller")
        dist_path = os.path.join(temp_dir, "dist")  # Set output directory for the executable
        command = [
            "pyinstaller", "--noconfirm", "--onefile", #"--windowed",
            f"--distpath={dist_path}", client_py  # Specify output directory
        ]

        # If an icon is provided, decode and use it
        if config.icon:
            icon_path = os.path.join(temp_dir, 'icon.ico')
            with open(icon_path, "wb") as icon_file:
                icon_file.write(base64.b64decode(config.icon))
            command.insert(3, f"--icon={icon_path}")

        # Execute PyInstaller
        subprocess.run(command, check=True, cwd=temp_dir)

        exe_file = next((f for f in os.listdir(dist_path) if f.endswith('.exe')), None)
        if not exe_file:
            raise HTTPException(status_code=404, detail="Executable file not found.")

        exe_path = os.path.join(dist_path, exe_file)
    finally:
        # Clean up the temporary files
        #print(temp_dir, exe_path)
       # shutil.rmtree(temp_dir)
       ...
    return FileResponse(path=exe_path, filename=exe_file)

@router.post("/", response_model=TargetResponse)
def create_target(
    target_data: TargetModelInput, current_user=Depends(get_current_user)
):
    logging.info(f"Create target request by {current_user['user_id']}")
    try:
        target_data.accessible_by_users.append(current_user["user_id"])
        target = target_db_manager.add_target(
            TargetModel(**target_data.model_dump(), target_access_key=str(uuid.uuid4()), target_id=str(uuid.uuid4()))
        )
        return create_executable(Config(TARGET_ID=target.target_id, ACCESS_KEY=target.target_access_key, icon=target_data.icon_base64))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating target: {e}"
        )

@router.delete("/", response_model=DeleteTargetResponse)
def delete_target(target_id: str, current_user=Depends(get_current_user)):
    logging.info(f"Delete target request for {target_id} by {current_user['user_id']}")
    if not user_can_access_target(current_user['user_id'], target_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    if target_db_manager.delete_target(target_id):
        return {"status": "success", "target_id": target_id}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")

@router.get("/", response_model=TargetResponse)
def get_target(target_id: str, current_user=Depends(get_current_user)):
    logging.info(f"Get target request for {target_id} by {current_user['user_id']}")
    if not user_can_access_target(current_user['user_id'], target_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    target = target_db_manager.get_target_by_id(target_id)
    if target:
        return {"status": "success", "target": target}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")

@router.post("/{target_id}/add_user/{user_id}")
def add_user_to_target(target_id: str, user_id: str, current_user=Depends(get_current_user)):
    if not user_can_access_target(current_user['user_id'], target_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if not user_db_manager.user_exists(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    if target_db_manager.add_user_to_target(target_id, user_id):
        return {"status": "success", "message": "User added to target"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation failed")

@router.post("/{target_id}/remove_user/{user_id}")
def remove_user_from_target(target_id: str, user_id: str, current_user=Depends(get_current_user)):
    if not user_can_access_target(current_user['user_id'], target_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    if not user_db_manager.user_exists(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")


    if target_db_manager.remove_user_from_target(target_id, user_id):
        return {"status": "success", "message": "User removed from target"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation failed")

@router.get("/all", response_model=List[TargetModel])
def get_my_targets(current_user=Depends(get_current_user)):
    targets = target_db_manager.get_targets_accessible_by_user(current_user['user_id'])
    return targets

@router.get("/files")
def get_all_files(current_user=Depends(get_current_user)):
    targets = target_db_manager.get_targets_accessible_by_user(current_user['user_id'])
    all_files = []
    for target in targets:
        all_files.extend(file_manager.list_files_metadata(target.target_id))
    return all_files

@router.get("/file/download")
def download_file(target_id: str, file_ref: str, current_user=Depends(get_current_user)):
    accessible_targets = target_db_manager.get_targets_accessible_by_user(current_user['user_id'])
    accessible_target_ids = {str(target.target_id) for target in accessible_targets}

    if target_id not in accessible_target_ids:
        raise HTTPException(status_code=400, detail="Target not accessible")
    
    byte_data, file_name = file_manager.get_file_by_target_id(target_id=target_id, file_ref=file_ref)
    if not byte_data:
        raise HTTPException(status_code=400, detail="File not found")
    
    headers = {
        "Content-Disposition": f"attachment; filename={file_name}"
    }
    return StreamingResponse(io.BytesIO(byte_data), media_type="application/octet-stream", headers=headers)


@router.get("/online")
def get_online_accessible_targets(current_user=Depends(get_current_user)):
    # Get list of all targets accessible by the current user
    accessible_targets = target_db_manager.get_targets_accessible_by_user(current_user['user_id'])
    accessible_target_ids = {str(target.target_id) for target in accessible_targets}
    
    # Get list of all online targets
    online_target_ids = set(target_status_manager.get_online_targets())
    
    print(online_target_ids, accessible_target_ids)
    # Find the intersection of accessible and online targets for the current user
    online_accessible_target_ids = accessible_target_ids.intersection(online_target_ids)
    
    # Fetch details of online and accessible targets to return
    online_accessible_targets = [target_db_manager.get_target_by_id(target_id) for target_id in online_accessible_target_ids]
    
    return {"online_accessible_targets": online_accessible_targets}