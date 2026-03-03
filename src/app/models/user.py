# Helper para UUID compatível com SQLite e Postgres
from src.app.core.database import Base
import uuid
from sqlalchemy import Column, String, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(Text)
    role = Column(String(50), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("ChatSession", back_populates="user")
