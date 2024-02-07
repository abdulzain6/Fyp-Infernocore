from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from ..auth import get_current_user, get_user_id
from ..globals import (
    user_db_manager,
)
from api.lib.database import UserModel
import logging

router = APIRouter()


class UserResponse(BaseModel):
    status: str
    error: str
    user: UserModel


class DeleteUserResponse(BaseModel):
    status: str
    error: str
    user: int



@router.post("/", response_model=UserResponse, tags=["user"])
def create_user(
    current_user=Depends(get_current_user),
):
    logging.info(
        f"Create user request from {current_user['user_id']}, {current_user['email']}"
    )
    try:
        user = user_db_manager.add_user(
            UserModel(
                uid=current_user["user_id"],
                email=current_user["email"],
            )
        )
        return {"status": "success", "error": "", "user": user}
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error Registering user, {e}"
        ) from e
        

@router.delete("/", response_model=DeleteUserResponse, tags=["user"])
def delete_user(
    user_id=Depends(get_user_id)
):
    logging.info(f"Delete user request from {user_id}")
    user = user_db_manager.delete_user(user_id)
    if user == 0:
        logging.error(f"User not found {user_id}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return {"status": "success", "error": "", "user": user}


@router.get("/", response_model=UserResponse, tags=["user"])
def get_user(
    current_user=Depends(get_current_user),
):
    logging.info(f"Get user request from {current_user['user_id']}")
    if user := user_db_manager.get_user_by_uid(current_user["user_id"]):
        return {"status": "success", "error": "", "user": user}

    user = user_db_manager.add_user(
        UserModel(
            uid=current_user["user_id"],
            email=current_user["email"],
        )
    )
    return {"status": "success", "error": "", "user": user}