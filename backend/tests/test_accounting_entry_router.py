import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import date, datetime

from backend.src.main import app
from backend.src.api.accounting_entry_router import get_accounting_entry_service
from backend.src.schemas.accounting_entry import AccountingEntryResponse
from backend.src.models.accounting_entry import AccountingEntry

@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)

@pytest.fixture
def mock_accounting_entry_service():
    mock_service = Mock()
    
    # Mock the behavior of create_accounting_entry
    mock_entry = AccountingEntry(
        id=1,
        date=date.today(),
        document_type="Invoice",
        description="Test Entry",
        amount=100.00,
        vat=5.0,
        recorder_id="test_user",
        remarks="Test remarks",
        proof_attachment_link="http://mock-gcs-link/proof",
        pdf_unique_ref_number="REF-mock-123",
        gcs_pdf_link="http://mock-gcs-link/pdf",
        created_at=datetime.now()
    )
    mock_service.create_accounting_entry.return_value = mock_entry
    return mock_service

@pytest.fixture(autouse=True)
def override_accounting_entry_service(test_client, mock_accounting_entry_service):
    app.dependency_overrides[get_accounting_entry_service] = lambda: mock_accounting_entry_service
    yield
    app.dependency_overrides.clear()

def test_create_accounting_entry_endpoint(test_client, mock_accounting_entry_service):
    payload = {
        "date": str(date.today()),
        "document_type": "Invoice",
        "description": "Test Entry",
        "amount": 100.00,
        "vat": 5.0,
        "recorder_id": "test_user",
        "remarks": "Test remarks",
        "attach_proof_base64": "JVBERi0xLjQKJcOkw..."
    }
    response = test_client.post("/api/v1/accounting-entries", json=payload)

    assert response.status_code == 201
    mock_accounting_entry_service.create_accounting_entry.assert_called_once()

    response_data = response.json()
    assert response_data["recorder_id"] == "test_user"
    assert "gcs_pdf_link" in response_data
    assert "proof_attachment_link" in response_data
    assert "pdf_unique_ref_number" in response_data
    assert "id" in response_data
    assert isinstance(response_data["id"], str)
    assert "created_at" in response_data

def test_create_accounting_entry_invalid_input(test_client):
    payload = {
        "date": "2025-12-30", # Future date
        "document_type": "Invoice",
        "description": "Test Entry",
        "amount": 0, # Amount <= 0
        "vat": 8.0, # VAT > 7
        "recorder_id": "test_user",
        "remarks": "Test remarks",
        "attach_proof_base64": "JVBERi0xLjQKJcOkw..."
    }
    response = test_client.post("/api/v1/accounting-entries", json=payload)
    assert response.status_code == 400
    assert "detail" in response.json()
