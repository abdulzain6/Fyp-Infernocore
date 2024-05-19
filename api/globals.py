from api.lib.database.redis_data_stores import RedisCommandStore
from .lib.database import UserDBManager, TargetDBManager, TargetStatusManager, UserFileManager
from .utils import get_script_path_and_append
from redis import asyncio as aioredis
import os
import redis
import dotenv

dotenv.load_dotenv("api/.env")
redis_client_aio = aioredis.Redis.from_url(os.getenv("REDIS_URL"))
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

BASE_URL = os.getenv("BASE_URL", "35.244.12.135")
CLIENT_FOLDER = get_script_path_and_append(["client"])
MAX_COMMAND_LIFE = os.getenv("MAX_COMMAND_LIFE", 30)

print(f"Client path: {CLIENT_FOLDER}")

user_db_manager = UserDBManager(
    os.getenv("MONGODB_URL"), os.getenv("DATABASE_NAME", "infernocore")
)
target_db_manager = TargetDBManager(
    os.getenv("MONGODB_URL"), os.getenv("DATABASE_NAME", "infernocore")
)
file_manager = UserFileManager(
    os.getenv("MONGODB_URL"), os.getenv("DATABASE_NAME", "infernocore")
)
target_status_manager = TargetStatusManager(redis_client)
command_store = RedisCommandStore(redis_client)