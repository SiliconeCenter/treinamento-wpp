from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..core.database import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nome = Column(String(255), nullable=False)
    perfil = Column(Text, nullable=False)
    objetivo = Column(Text, nullable=False)
    instrucao = Column(Text, nullable=False)
