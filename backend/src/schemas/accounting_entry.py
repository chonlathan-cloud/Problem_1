from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class CreateAccountingEntryRequest(BaseModel):
    date: date = Field(..., description="The date of the accounting entry (YYYY-MM-DD).")
    document_type: str = Field(..., description="The type of document.")
    description: str = Field(..., description="A detailed description of the entry.")
    amount: float = Field(..., gt=0, description="The monetary amount of the entry. Must be greater than 0.")
    vat: float = Field(..., ge=0, le=7, description="The Value Added Tax percentage. Must be between 0 and 7 (inclusive).")
    recorder_id: str = Field(..., description="Identifier of the employee who recorded the entry.")
    remarks: Optional[str] = Field(None, description="Additional remarks or notes.")
    attach_proof_base64: str = Field(..., description="Base64 encoded content of the attached proof file (e.g., PDF, image).")

    @validator('date')
    def date_not_in_future(cls, v):
        if v > date.today():
            raise ValueError('Date cannot be in the future')
        return v

class AccountingEntryResponse(BaseModel):
    id: str
    date: date
    document_type: str
    description: str
    amount: float
    vat: float
    recorder_id: str
    remarks: Optional[str]
    proof_attachment_link: Optional[str]
    pdf_unique_ref_number: Optional[str]
    gcs_pdf_link: Optional[str]
    created_at: str

    class Config:
        orm_mode = True # Enable ORM mode for SQLAlchemy models
