from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PersonaBase(BaseModel):
    nome: str
    perfil: str
    objetivo: str
    instrucao: str


class PersonaCreate(PersonaBase):
    """Usado para a criação e extração via IA"""

    pass


class PersonaResponse(PersonaBase):
    """Usado para retornar os dados da Persona na API"""

    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
