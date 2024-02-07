from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from ..auth import get_current_user
from ..globals import target_db_manager, user_db_manager, target_status_manager
from api.lib.database import TargetModel
import logging
import uuid

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



def user_can_access_target(user_id: str, target_id: str) -> bool:
    return target_db_manager.is_target_accessible_by_user(target_id, user_id)


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
        return {"status": "success", "target": target}
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