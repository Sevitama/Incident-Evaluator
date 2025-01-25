from sqlalchemy.orm import Session, mapped_column
from sqlalchemy import (
    create_engine,
    select,
    update,
)
from typing import List, Optional
from datetime import datetime
from .base import Base
from .incident import Incident
from .rule_data import RuleData
from .threat_history import ThreatHistory

class DatabaseManager:
    """Manager for database operations."""

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self._setup_db()

    def _setup_db(self) -> None:
        """Sets up the database by creating tables."""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Creates a new session for database operations."""
        return Session(self.engine)

    def create_rule_data(self, rule_name: str, signal_quality: float, rel_cost_analyst: float, rel_cost_damage: float) -> None:
        """Adds a new rule data entry to the database."""
        with self.get_session() as session:
            new_rule_data = RuleData(
                rule_name=rule_name,
                signal_quality=signal_quality,
                rel_cost_analyst=rel_cost_analyst,
                rel_cost_damage=rel_cost_damage
            )
            session.add(new_rule_data)
            session.commit()

    def create_new_threat_history(self, incident_id: Optional[int], threat_level: float, timestamp: datetime) -> None:
        """Creates a new threat history entry and logs the event."""
        with self.get_session() as session:
            rounded_threat_level = round(threat_level, 2)
            new_threat_history = ThreatHistory(
                incident_id=incident_id, 
                threat_level=rounded_threat_level,
                timestamp=timestamp
            )
            session.add(new_threat_history)
            session.commit()

    def create_incident(self, incident_id: int, rule_id: int, incident_start: datetime) -> int:
        """Creates a new incident entry."""
        with self.get_session() as session:
            new_incident = Incident(
                incident_id=incident_id,
                incident_rule=rule_id,
                incident_start=incident_start,
                incident_result=None,
            )
            session.add(new_incident)
            session.commit()
            return new_incident.incident_id

    def update_incident_result(self, incident_id: int, incident_result: str) -> None:
        """Updates the result of an incident."""
        with self.get_session() as session:
            session.execute(
                update(Incident)
                .where(Incident.incident_id == incident_id)
                .values(incident_result=incident_result)
            )
            session.commit()

    def get_rule_data(self, rule_name: str) -> RuleData:
        """Fetches rule data by rule name."""
        with self.get_session() as session:
            return session.execute(
                select(RuleData).where(RuleData.rule_name == rule_name)
            ).scalars().one()

    def get_last_threat_history(self) -> ThreatHistory:
        """Fetches the last entry in threat history."""
        with self.get_session() as session:
            return session.execute(
                select(ThreatHistory).order_by(ThreatHistory.threat_history_id.desc())
            ).scalars().first()
