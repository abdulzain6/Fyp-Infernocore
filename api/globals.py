from .lib.database import UserDBManager, TargetDBManager, TargetStatusManager
from redis import asyncio as aioredis
import os
import redis
import dotenv

redis_client_aio = aioredis.Redis(host='localhost', port=6379, db=0)
redis_client = redis.Redis(host='localhost', port=6379, db=0)


dotenv.load_dotenv()

user_db_manager = UserDBManager(
    os.getenv("MONGODB_URL"), os.getenv("DATABASE_NAME", "infernocore")
)
target_db_manager = TargetDBManager(
    os.getenv("MONGODB_URL"), os.getenv("DATABASE_NAME", "infernocore")
)
target_status_manager = TargetStatusManager(redis_client)