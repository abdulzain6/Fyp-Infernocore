from fastapi import FastAPI
from .routers.users import router as users_router
from .routers.targets import router as target_router
from .routers.send_recieve_target import router as send_recieve_target_router
from .routers.send_recieve_attacker import router as send_recieve_attacker
from scalar_fastapi import get_scalar_api_reference
import logging


logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Infernocore"
    )

app.include_router(users_router, prefix="/users", tags=["user"])
app.include_router(target_router, prefix="/target", tags=["target"])
app.include_router(send_recieve_target_router, prefix="/io-target", tags=["io-target"])
app.include_router(send_recieve_attacker, prefix="/io-attacker", tags=["io-attacker"])