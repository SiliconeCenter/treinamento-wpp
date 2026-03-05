from fastapi import FastAPI
from src.app.core.database import Base, engine

from src.app.api.v1.auth import auth_router
from src.app.api.v1.user import users_router
from src.app.api.v1.personas import persona_router

app = FastAPI()


@app.on_event("startup")
def configure_db():
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(persona_router)
