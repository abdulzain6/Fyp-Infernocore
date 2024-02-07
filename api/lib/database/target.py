from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection

class TargetModel(BaseModel):
    target_id: str
    name: str
    accessible_by_users: List[str] 
    target_access_key: str

class TargetDBManager:
    def __init__(self, connection_string: str, database_name: str) -> None:
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.target_collection: Collection = self.db["targets"]
        self.target_collection.create_index("target_id", unique=True)

    def add_target(self, target_model: TargetModel) -> TargetModel:
        if self.target_exists(target_model.target_id):
            raise ValueError("Target already exists")
        self.target_collection.insert_one(target_model.model_dump())
        return target_model
    
    def get_target_by_id(self, target_id: str) -> Optional[TargetModel]:
        target_data = self.target_collection.find_one({"target_id": target_id})
        if target_data:
            return TargetModel(**target_data)
        return None

    def target_exists(self, target_id: str) -> bool:
        return self.target_collection.count_documents({"target_id": target_id}, limit=1) > 0

    def get_all_targets(self) -> List[TargetModel]:
        all_targets = list(self.target_collection.find({}))
        return [TargetModel(**doc) for doc in all_targets]

    def update_target(self, target_id: str, **kwargs: Dict[str, Any]) -> int:
        if "target_id" in kwargs:
            raise ValueError("Changing 'target_id' is not allowed.")
        result = self.target_collection.update_one({"target_id": target_id}, {"$set": kwargs})
        return result.modified_count

    def delete_target(self, target_id: str) -> bool:
        self.target_collection.delete_one({"target_id": target_id})
        return True

    def add_user_to_target(self, target_id: str, user_id: str) -> bool:
        if not self.target_exists(target_id):
            raise ValueError("Target does not exist")
        result = self.target_collection.update_one(
            {"target_id": target_id},
            {"$addToSet": {"accessible_by_users": user_id}}
        )
        return result.modified_count > 0

    def remove_user_from_target(self, target_id: str, user_id: str) -> bool:
        result = self.target_collection.update_one(
            {"target_id": target_id},
            {"$pull": {"accessible_by_users": user_id}}
        )
        
        return result.modified_count > 0
    
    def is_target_accessible_by_user(self, target_id: str, user_id: str) -> bool:
        target_data = self.target_collection.find_one({"target_id": target_id, "accessible_by_users": user_id})
        return target_data is not None

    def get_targets_accessible_by_user(self, user_id: str) -> List[TargetModel]:
        targets = list(self.target_collection.find({"accessible_by_users": user_id}))
        return [TargetModel(**doc) for doc in targets]
