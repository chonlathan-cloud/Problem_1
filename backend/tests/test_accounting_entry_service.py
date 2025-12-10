import pytest
from unittest.mock import Mock
from datetime import date, datetime
from backend.src.services.accounting_entry_service import AccountingEntryService
from backend.src.schemas.accounting_entry import CreateAccountingEntryRequest

@pytest.fixture
def mock_db_session():
    return Mock()

@pytest.fixture
def mock_pdf_generator():
    mock = Mock()
    mock.generate_accounting_entry_pdf.return_value = Mock(getvalue=lambda: b"mock_pdf_content")
    return mock

@pytest.fixture
def mock_gcs_client():
    mock = Mock()
    mock.upload_file.return_value = "http://mock-gcs-link"
    return mock

@pytest.fixture
def mock_audit_log_service():
    return Mock()

@pytest.fixture
def accounting_entry_service(
    mock_db_session,
    mock_pdf_generator,
    mock_gcs_client,
    mock_audit_log_service
):
    return AccountingEntryService(
        mock_db_session,
        mock_pdf_generator,
        mock_gcs_client,
        mock_audit_log_service
    )

def test_create_accounting_entry(accounting_entry_service, mock_db_session, mock_pdf_generator, mock_gcs_client, mock_audit_log_service):
    entry_request = CreateAccountingEntryRequest(
        date=date.today(),
        document_type="Invoice",
        description="Test Entry",
        amount=100.00,
        vat=5.0,
        recorder_id="test_user",
        remarks="Test remarks",
        attach_proof_base64="JVBERi0xLjQKJcOkw..." # Dummy base64
    )

    # Mock db_entry properties that would be set after commit/refresh
    mock_db_entry = Mock()
    mock_db_entry.id = 1
    mock_db_entry.date = entry_request.date
    mock_db_entry.document_type = entry_request.document_type
    mock_db_entry.description = entry_request.description
    mock_db_entry.amount = entry_request.amount
    mock_db_entry.vat = entry_request.vat
    mock_db_entry.recorder_id = entry_request.recorder_id
    mock_db_entry.remarks = entry_request.remarks
    mock_db_entry.gcs_pdf_link = None # Will be set later
    mock_db_entry.proof_attachment_link = None # Will be set later
    mock_db_entry.pdf_unique_ref_number = None # Will be set later
    mock_db_entry.created_at = datetime.now() # Mock datetime

    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 1) or setattr(obj, 'created_at', datetime.now())


    result = accounting_entry_service.create_accounting_entry(entry_request)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called()
    mock_db_session.refresh.assert_called()
    mock_pdf_generator.generate_accounting_entry_pdf.assert_called_once()
    mock_gcs_client.upload_file.call_count == 2 # Once for PDF, once for attachment
    mock_audit_log_service.log_event.assert_called_once_with(
        user_id="test_user",
        action_type="ENTRY_CREATED",
        target_entry_id=mock_db_entry.id,
        details_of_change=f"New accounting entry {mock_db_entry.id} created."
    )

    assert result.recorder_id == "test_user"
    assert isinstance(result.id, int)
    assert result.id == 1
    assert result.gcs_pdf_link is not None
    assert result.proof_attachment_link is not None
    assert result.pdf_unique_ref_number is not None
