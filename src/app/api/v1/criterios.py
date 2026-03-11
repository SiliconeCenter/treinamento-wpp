from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.models.models_treinmento_wpp import EvaluationCriteria
from src.app.schemas.criterio.criterios_schemas import CriterioCreate, CriterioOutput
from src.app.security.password import get_admin_user

criterios_router = APIRouter(prefix="/creterios", tags=["criterios"])


@criterios_router.post("/criterio_create", response_model=CriterioOutput)
def criterio_create(
    criterio: CriterioCreate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[dict, Depends(get_admin_user)],
):
    novo_criterio = EvaluationCriteria(
        checklist_id=criterio.checklist_id,
        nome=criterio.nome,
        descricao=criterio.descricao,
        peso=criterio.peso,
    )

    db.add(novo_criterio)
    db.commit()
    db.refresh(novo_criterio)

    return novo_criterio


@criterios_router.get("/paginate", response_model=Page[CriterioOutput])
def list_all_criterios(
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[dict, Depends(get_admin_user)],
):
    query = db.query(EvaluationCriteria)

    return paginate(query)
