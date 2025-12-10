from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from .base import Base

class AuditLogEntry(Base):
    __tablename__ = "audit_log_entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    user_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    target_entry_id = Column(Integer, ForeignKey("accounting_entries.id"), nullable=False)
    details_of_change = Column(Text, nullable=True)
