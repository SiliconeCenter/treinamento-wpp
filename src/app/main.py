from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.app.api.v1.auth import auth_router
from src.app.api.v1.checklist import checklist_router
from src.app.api.v1.criterios import criterios_router
from src.app.api.v1.personas import persona_router
from src.app.api.v1.user import users_router
from src.app.core.database import Base, engine

app = FastAPI()


@app.on_event("startup")
def configure_db():
    Base.metadata.create_all(bind=engine)


add_pagination(app)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(persona_router)
app.include_router(checklist_router)
app.include_router(criterios_router)
