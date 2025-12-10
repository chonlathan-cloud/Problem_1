from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.src.schemas.accounting_entry import CreateAccountingEntryRequest, AccountingEntryResponse
from backend.src.services.accounting_entry_service import AccountingEntryService
from backend.src.services.pdf_generator import PDFGenerator
from backend.src.services.gcs_client import GCSClient
from backend.src.services.audit_log_service import AuditLogService, AbstractAuditLogService
from backend.src.database import get_db
from backend.src.auth.auth_bearer import verify_token

router = APIRouter()

# Dependency for AccountingEntryService
def get_accounting_entry_service(db: Session = Depends(get_db)) -> AccountingEntryService:
    pdf_generator = PDFGenerator()
    gcs_client = GCSClient()
    audit_log_service: AbstractAuditLogService = AuditLogService() # Concrete implementation for now
    return AccountingEntryService(db, pdf_generator, gcs_client, audit_log_service)

@router.post(
    "/accounting-entries",
    response_model=AccountingEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new accounting entry",
    description="Allows an employee to record a new accounting entry, generate a PDF, upload to GCS, and log the action."
)
def create_accounting_entry(
    request: CreateAccountingEntryRequest,
    accounting_entry_service: AccountingEntryService = Depends(get_accounting_entry_service),
    user_id: str = Depends(verify_token) # Add authentication dependency
):
    try:
        # The user_id obtained from the token can be used here if needed, 
        # e.g., to set request.recorder_id if not explicitly provided by the user
        created_entry = accounting_entry_service.create_accounting_entry(request)
        return AccountingEntryResponse(
            id=str(created_entry.id),
            date=created_entry.date,
            document_type=created_entry.document_type,
            description=created_entry.description,
            amount=created_entry.amount,
            vat=created_entry.vat,
            recorder_id=created_entry.recorder_id,
            remarks=created_entry.remarks,
            proof_attachment_link=created_entry.proof_attachment_link,
            pdf_unique_ref_number=created_entry.pdf_unique_ref_number,
            gcs_pdf_link=created_entry.gcs_pdf_link,
            created_at=created_entry.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
