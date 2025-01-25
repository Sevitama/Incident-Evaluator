from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    Integer,
    Float,
    String,
)
from .base import Base

class RuleData(Base):
    """Model representing rule data."""
    __tablename__ = "rule_data"

    rule_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    rule_name = mapped_column(String, nullable=False)
    signal_quality = mapped_column(Float, nullable=False)
    rel_cost_analyst = mapped_column(Float, nullable=False)
    rel_cost_damage = mapped_column(Float, nullable=False)