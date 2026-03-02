from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..core.database import Base


class EvaluationCriteria(Base):
    __tablename__ = "evaluation_criteria"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    persona_id = Column(UUID(as_uuid=True), ForeignKey("personas.id"))

    nome = Column(String(255))
    descricao = Column(Text)

    peso = Column(Integer)
