import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.app.core.database import Base


# Helper para UUID compatível com SQLite e Postgres
def generate_uuid():
    return str(uuid.uuid4())


class CriteriaResult(Base):
    __tablename__ = "criteria_results"

    id = Column(String, primary_key=True, default=generate_uuid)
    analysis_id = Column(String, ForeignKey("session_analysis.id"))
    criteria_id = Column(String, ForeignKey("evaluation_criteria.id"))
    score = Column(Integer)
    feedback = Column(Text)

    analysis = relationship("SessionAnalysis", back_populates="results")
