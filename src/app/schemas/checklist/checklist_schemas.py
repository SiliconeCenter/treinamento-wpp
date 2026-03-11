from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ChecklistCreate(BaseModel):
    nome: str


class ChecklistOutput(ChecklistCreate):
    id: UUID
    created_at: datetime
