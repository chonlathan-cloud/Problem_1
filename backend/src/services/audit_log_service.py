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

class AuditLogService(AbstractAuditLogService):
    # For now, a simple in-memory logger or placeholder.
    # This will be replaced with a proper SQLAlchemy/DB implementation later.
    def log_event(self,
                  user_id: str,
                  action_type: str,
                  target_entry_id: int,
                  details_of_change: Optional[str] = None) -> None:
        print(f"[AUDIT LOG] {datetime.now()} - User: {user_id}, Action: {action_type}, "
              f"Target ID: {target_entry_id}, Details: {details_of_change}")
