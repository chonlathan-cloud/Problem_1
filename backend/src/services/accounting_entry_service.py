from sqlalchemy.orm import Session
from backend.src.models.accounting_entry import AccountingEntry
from backend.src.schemas.accounting_entry import CreateAccountingEntryRequest
from backend.src.services.pdf_generator import PDFGenerator
from backend.src.services.gcs_client import GCSClient
from backend.src.services.audit_log_service import AbstractAuditLogService
from datetime import datetime
import base64

class AccountingEntryService:
    def __init__(self, db: Session, pdf_generator: PDFGenerator, gcs_client: GCSClient, audit_log_service: AbstractAuditLogService):
        self.db = db
        self.pdf_generator = pdf_generator
        self.gcs_client = gcs_client
        self.audit_log_service = audit_log_service

    def create_accounting_entry(self, entry_data: CreateAccountingEntryRequest) -> AccountingEntry:
        db_entry = AccountingEntry(
            date=entry_data.date,
            document_type=entry_data.document_type,
            description=entry_data.description,
            amount=entry_data.amount,
            vat=entry_data.vat,
            recorder_id=entry_data.recorder_id,
            remarks=entry_data.remarks,
        )
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)

        # Generate PDF and unique reference number
        unique_ref_number = f"REF-{datetime.now().strftime("%Y%m%d-%H%M%S-%f")}"
        pdf_buffer = self.pdf_generator.generate_accounting_entry_pdf({
            "date": entry_data.date.isoformat(),
            "document_type": entry_data.document_type,
            "description": entry_data.description,
            "amount": entry_data.amount,
            "vat": entry_data.vat,
            "recorder_id": entry_data.recorder_id,
            "remarks": entry_data.remarks,
            "pdf_unique_ref_number": unique_ref_number
        })
        db_entry.pdf_unique_ref_number = unique_ref_number

        # Upload PDF to GCS
        pdf_filename = f"accounting_entries/pdf/{unique_ref_number}.pdf"
        gcs_pdf_link = self.gcs_client.upload_file(pdf_buffer.getvalue(), pdf_filename, content_type="application/pdf")
        db_entry.gcs_pdf_link = gcs_pdf_link

        # Upload proof attachment to GCS
        proof_filename = f"accounting_entries/proof/{db_entry.id}-{datetime.now().strftime("%Y%m%d%H%M%S")}.bin"
        proof_content = base64.b64decode(entry_data.attach_proof_base64)
        proof_attachment_link = self.gcs_client.upload_file(proof_content, proof_filename)
        db_entry.proof_attachment_link = proof_attachment_link

        self.db.commit()
        self.db.refresh(db_entry)

        self.audit_log_service.log_event(
            user_id=entry_data.recorder_id,
            action_type="ENTRY_CREATED",
            target_entry_id=db_entry.id,
            details_of_change=f"New accounting entry {db_entry.id} created."
        )

        return db_entry
