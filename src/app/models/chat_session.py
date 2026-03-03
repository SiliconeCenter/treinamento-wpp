import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.app.core.database import Base


# Helper para UUID compatível com SQLite e Postgres
def generate_uuid():
    return str(uuid.uuid4())


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    persona_id = Column(String, ForeignKey("personas.id"))
    status = Column(String(50))
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)

    user = relationship("User", back_populates="sessions")
    persona = relationship("Persona", back_populates="sessions")
    messages = relationship("ChatMessage", back_populates="session")
    analysis = relationship("SessionAnalysis", back_populates="session", uselist=False)
