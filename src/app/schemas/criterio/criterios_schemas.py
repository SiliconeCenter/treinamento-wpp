from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CriterioCreate(BaseModel):
    checklist_id: UUID
    nome: str
    descricao: str
    peso: int


class CriterioOutput(CriterioCreate):
    id: UUID
    created_at: datetime
