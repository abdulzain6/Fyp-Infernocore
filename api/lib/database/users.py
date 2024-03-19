from typing import Any, Dict, List, Optional
from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo import MongoClient
from gridfs import GridFSBucket


class UserModel(BaseModel):
    uid: str
    email: str

class FileModel(BaseModel):
    target_id: str
    target_name: str
    file_reference: str

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

class UserFileManager:
    def __init__(self, connection_string: str, database_name: str) -> None:
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.gridfs_bucket = GridFSBucket(self.db)
        self.file_collection = self.db["file_metadata"]

    def add_file(self, target_id: str, target_name: str, file_data: bytes, filename: str) -> FileModel:
        # Check if the file metadata already exists for the given target_id and target_name
        if self.file_collection.find_one({"target_id": target_id, "target_name": target_name}):
            raise ValueError("File with this target_name already exists for the target ID.")

        # Store the file in GridFS
        file_id = self.gridfs_bucket.upload_from_stream(filename, file_data)

        # Create and store file metadata
        file_model = FileModel(target_id=target_id, target_name=target_name, file_reference=str(file_id))
        self.file_collection.insert_one(file_model.model_dump())

        return file_model

    def get_file_by_target_id(self, target_id: str, file_ref: str) -> Optional[bytes]:
        file_metadata = self.file_collection.find_one({"target_id": target_id, "file_reference" : file_ref})
        if not file_metadata:
            return None

        file_id = file_metadata["file_reference"]
        file_stream = self.gridfs_bucket.open_download_stream(ObjectId(file_id))
        return file_stream.read(), file_stream.filename

    def delete_file(self, target_id: str, target_name: str) -> bool:
        file_metadata = self.file_collection.find_one({"target_id": target_id, "target_name": target_name})
        if not file_metadata:
            return False

        file_id = file_metadata["file_reference"]

        # Delete the file from GridFS
        self.gridfs_bucket.delete(ObjectId(file_id))

        # Delete the metadata
        self.file_collection.delete_one({"target_id": target_id, "target_name": target_name})

        return True

    def list_files_metadata(self, target_id: str) -> List[FileModel]:
        """
        Lists all files' metadata for a given target ID.

        :param target_id: The unique identifier for the target.
        :return: A list of FileModel instances representing each file's metadata.
        """
        files_metadata = self.file_collection.find({"target_id": target_id})
        return [FileModel(**metadata) for metadata in files_metadata]
