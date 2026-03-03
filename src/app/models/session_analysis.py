import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.app.core.database import Base


# Helper para UUID compatível com SQLite e Postgres
def generate_uuid():
    return str(uuid.uuid4())


class SessionAnalysis(Base):
    __tablename__ = "session_analysis"

    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, ForeignKey("chat_sessions.id"))
    score_total = Column(Integer)
    feedback_geral = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="analysis")
    results = relationship("CriteriaResult", back_populates="analysis")
