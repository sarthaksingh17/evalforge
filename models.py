from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.sql import func
from database import Base
import uuid

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt = Column(String, nullable=False)
    response = Column(String, nullable=False)
    rubric = Column(String, nullable=True)
    score = Column(Integer, nullable=False)
    reasoning = Column(String, nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())