from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from .base import Base

class Incident(Base):
    """Model representing incidents."""
    __tablename__ = "incident"

    incident_id = mapped_column(Integer, primary_key=True)
    incident_rule = mapped_column(Integer, ForeignKey("rule_data.rule_id"), nullable=False)
    incident_start = mapped_column(DateTime, nullable=False)
    incident_result = mapped_column(String, nullable=True)