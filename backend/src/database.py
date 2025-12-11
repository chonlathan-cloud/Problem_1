from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.src.config import settings
from backend.src.models.base import Base
from backend.src.models.audit_log import AuditLog
from backend.src.models.user import User

#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # This is for creating tables during development/testing. 
    # In production, use Alembic migrations.
    Base.metadata.create_all(bind=engine)
