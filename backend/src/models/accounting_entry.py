from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class AccountingEntry(Base):
    __tablename__ = "accounting_entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    document_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    vat = Column(Numeric(4, 2), nullable=False)
    recorder_id = Column(String, nullable=False) # Assuming User entity is external or will be defined later
    remarks = Column(String, nullable=True)
    proof_attachment_link = Column(String, nullable=True)
    pdf_unique_ref_number = Column(String, unique=True, nullable=True)
    gcs_pdf_link = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
