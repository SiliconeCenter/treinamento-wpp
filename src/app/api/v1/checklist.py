from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.models.models_treinmento_wpp import Checklist
from src.app.schemas.checklist.checklist_schemas import ChecklistCreate, ChecklistOutput
from src.app.security.password import get_admin_user

checklist_router = APIRouter(prefix="/checklist", tags=["checklist"])


@checklist_router.post("/create_checklist", status_code=status.HTTP_201_CREATED)
def checklist_create(
    data: ChecklistCreate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[dict, Depends(get_admin_user)],
):
    nome_existe = db.query(Checklist).filter(Checklist.nome == data.nome).first()

    if nome_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Checklist name already exists",
        )

    novo_cl = Checklist(nome=data.nome)

    db.add(novo_cl)
    db.commit()
    db.refresh(novo_cl)

    return {
        "id": novo_cl.id,
        "nome": novo_cl.nome,
    }


@checklist_router.get("/paginate", response_model=Page[ChecklistOutput])
def list_all_checklist(
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[dict, Depends(get_admin_user)],
):
    query = db.query(Checklist)

    return paginate(query)
