from fastapi import FastAPI
from .routers.users import router as users_router
from .routers.targets import router as target_router
from .routers.send_recieve_target import router as send_recieve_target_router
from .routers.send_recieve_attacker import router as send_recieve_attacker
import logging


logging.basicConfig(level=logging.INFO)
app = FastAPI()


app.include_router(users_router, prefix="/users", tags=["user"])
app.include_router(target_router, prefix="/target", tags=["target"])
app.include_router(send_recieve_target_router, prefix="/io-target", tags=["io-target"])
app.include_router(send_recieve_attacker, prefix="/io-attacker", tags=["io-attacker"])