import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from src.app.core.database import Base


# Helper para UUID compatível com SQLite e Postgres
def generate_uuid():
    return str(uuid.uuid4())


class Persona(Base):
    __tablename__ = "personas"

    id = Column(String, primary_key=True, default=generate_uuid)
    nome = Column(String(255), nullable=False)
    perfil = Column(Text, nullable=False)
    objetivo = Column(Text, nullable=False)
    instrucao = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    criteria = relationship("EvaluationCriteria", back_populates="persona")
    sessions = relationship("ChatSession", back_populates="persona")
