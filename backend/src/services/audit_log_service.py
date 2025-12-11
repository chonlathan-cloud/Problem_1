from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class AbstractAuditLogService(ABC):
    @abstractmethod
    def log_event(self,
                  user_id: str,
                  action_type: str,
                  target_entry_id: int,
                  details_of_change: Optional[str] = None) -> None:
        """Logs an audit event."""
        pass

from sqlalchemy.orm import Session
from backend.src.models.audit_log import AuditLog

class AuditLogService(AbstractAuditLogService):
    def __init__(self, db: Session):
        self.db = db

    def log_event(self,
                  user_id: str,
                  action_type: str,
                  target_entry_id: int,
                  details_of_change: Optional[str] = None) -> None:
        audit_log = AuditLog(
            user_id=user_id,
            action_type=action_type,
            target_entry_id=target_entry_id,
            details=details_of_change
        )
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        print(f"[AUDIT LOG] Saved to DB - ID: {audit_log.id}")
