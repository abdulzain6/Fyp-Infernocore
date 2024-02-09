from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from fastapi import Depends, HTTPException, status
from .firebase import default_app
import logging


security = HTTPBearer()


def get_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    print("in")
    token = credentials.credentials
    try:
        return get_set_user_id(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def get_set_user_id(token):
    user = auth.verify_id_token(token, app=default_app)
    user_id = user["user_id"]
    logging.info("Verified token, storing in cache...")
    return user_id

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user = auth.verify_id_token(token, app=default_app)
        user_details = auth.get_user(user["user_id"])
        user_data = {
            "email": user_details.email,
            "user_id": user["user_id"],
            "display_name": user_details.display_name,
            "photo_url": user_details.photo_url,
        }
        return user_data
    except Exception as e:
        logging.error(f"Error in id token. {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
        


