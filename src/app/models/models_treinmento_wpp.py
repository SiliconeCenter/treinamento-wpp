import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    password_hash = Column(Text)
    role = Column(String(50), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("ChatSession", back_populates="user")


class Persona(Base):
    __tablename__ = "personas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checklist_name = Column(String(255), nullable=False)
    nome = Column(String(255), nullable=False)
    perfil = Column(Text, nullable=False)
    objetivo = Column(Text, nullable=False)
    instrucao = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("ChatSession", back_populates="persona")


class EvaluationCriteria(Base):
    __tablename__ = "evaluation_criteria"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checklist_id = Column(UUID(as_uuid=True))
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    peso = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    results = relationship("CriteriaResult", back_populates="criteria")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    persona_id = Column(UUID(as_uuid=True), ForeignKey("personas.id"))

    status = Column(String)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

    user = relationship("User", back_populates="sessions")
    persona = relationship("Persona", back_populates="sessions")

    messages = relationship("ChatMessage", back_populates="session")
    analysis = relationship("SessionAnalysis", back_populates="session", uselist=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"))

    sender = Column(String(50))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class SessionAnalysis(Base):
    __tablename__ = "session_analysis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"))

    score_total = Column(Integer)
    feedback_geral = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="analysis")
    criteria_results = relationship("CriteriaResult", back_populates="analysis")


class CriteriaResult(Base):
    __tablename__ = "criteria_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("session_analysis.id"))
    criteria_id = Column(UUID(as_uuid=True), ForeignKey("evaluation_criteria.id"))

    score = Column(Integer)
    feedback = Column(Text)

    analysis = relationship("SessionAnalysis", back_populates="criteria_results")
    criteria = relationship("EvaluationCriteria", back_populates="results")


class Checklist(Base):
    __tablename__ = "checklist"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
