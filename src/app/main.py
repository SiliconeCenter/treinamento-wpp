from fastapi import FastAPI

from src.app.api.v1.auth import auth_router

app = FastAPI()

app.include_router(auth_router)
