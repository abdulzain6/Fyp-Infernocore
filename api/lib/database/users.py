from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection


class UserModel(BaseModel):
    uid: str
    email: str

class UserDBManager:
    def __init__(
        self,
        connection_string: str,
        database_name: str,
    ) -> None:
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.user_collection: Collection = self.db["users"]
        self.user_collection.create_index("uid", unique=True)

    def add_user(self, user_model: UserModel) -> UserModel:
        if self.user_exists(user_model.uid):
            raise ValueError("User already exists")
        self.user_collection.insert_one(user_model.model_dump())
        return user_model
    
    def get_user_by_uid(self, uid: str) -> Optional[UserModel]:
        if user_data := self.user_collection.find_one({"uid": uid}):
            return UserModel(**user_data)
        return None

    def user_exists(self, uid: str) -> bool:
        return self.user_collection.count_documents({"uid": uid}, limit=1) > 0

    def get_all(self) -> List[UserModel]:
        all_users = list(self.user_collection.find({}))
        return [UserModel(**doc) for doc in all_users]

    def update_user(self, uid: str, **kwargs: Dict[str, Any]) -> int:
        if "uid" in kwargs:
            raise ValueError("Changing 'uid' is not allowed.")
        result = self.user_collection.update_one({"uid": uid}, {"$set": kwargs})
        return result.modified_count

    def delete_user(self, uid: str) -> bool:
        self.user_collection.delete_one({"uid": uid})
        return True