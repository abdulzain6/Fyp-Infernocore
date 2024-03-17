from api.lib.database.redis_data_stores import RedisCommandStore
from .lib.database import UserDBManager, TargetDBManager, TargetStatusManager
from redis import asyncio as aioredis
import os
import redis
import dotenv

dotenv.load_dotenv()
redis_client_aio = aioredis.Redis.from_url(os.getenv("REDIS_URL"))
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))


user_db_manager = UserDBManager(
    os.getenv("MONGODB_URL"), os.getenv("DATABASE_NAME", "infernocore")
)
target_db_manager = TargetDBManager(
    os.getenv("MONGODB_URL"), os.getenv("DATABASE_NAME", "infernocore")
)
target_status_manager = TargetStatusManager(redis_client)
command_store = RedisCommandStore(redis_client)