from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Float,
)
from .base import Base

class ThreatHistory(Base):
    """Model representing threat history."""
    __tablename__ = "threat_history"

    threat_history_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    threat_level = mapped_column(Float, nullable=False)
    incident_id = mapped_column(Integer, ForeignKey("incident.incident_id"), nullable=True)
    timestamp = mapped_column(DateTime, nullable=False)