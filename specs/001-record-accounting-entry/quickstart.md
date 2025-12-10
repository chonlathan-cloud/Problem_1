# Quickstart Guide: Record Accounting Entry and Generate PDF

This guide provides a high-level overview of how to get started with the "Record Accounting Entry and Generate PDF" feature.

## 1. Feature Overview

This feature provides a web-based interface for employees to efficiently record daily accounting entries. Upon successful submission and validation, the system automatically generates a PDF document of the entry, uploads it to Google Cloud Storage (GCS), and maintains an immutable audit log.

## 2. Employee Workflow (UI Interaction)

1.  **Access the Accounting Entry UI**: Employees will navigate to the designated web page for recording accounting entries.
2.  **Input Data**: Fill in all mandatory fields:
    *   **Date**: The date of the transaction.
    *   **Document Type**: e.g., Invoice, Receipt, Memo.
    *   **Description**: A clear summary of the transaction.
    *   **Amount**: The monetary value (must be greater than 0).
    *   **VAT**: The VAT percentage (must be between 0% and 7%).
    *   **Recorder**: Your employee ID or name.
    *   **Remarks**: Any additional notes (optional).
    *   **Attach Proof**: Upload a supporting document (e.g., a scan of an invoice).
3.  **Submit Entry**: Click the "Submit" or "Record Entry" button.
4.  **Confirmation**: Receive confirmation that the entry was successfully recorded. The system will then proceed with PDF generation, GCS upload, and audit logging in the background.

## 3. API Interaction (for Developers)

Developers can interact with the backend API to programmatically create accounting entries.

### Endpoint:

`POST /api/v1/accounting-entries`

### Request Body (JSON Example):

```json
{
  "date": "2025-12-09",
  "document_type": "Invoice",
  "description": "Office supplies purchase",
  "amount": 150.75,
  "vat": 5.0,
  "recorder_id": "EMP123",
  "remarks": "Urgent purchase",
  "attach_proof_base64": "JVBERi0xLjQKJcOkw..." 
}
```
*Note: `attach_proof_base64` expects the base64 encoded content of the proof file.*

### Expected Response:

Upon successful creation (HTTP 201 Created), the API will return details of the created entry, including links to the generated PDF and uploaded proof in GCS, and a unique PDF reference number.

## 4. Key Outcomes

*   A new accounting entry recorded in the system.
*   A PDF document, formatted to a standard template, generated with a unique reference number.
*   The generated PDF and attached proof document uploaded to Google Cloud Storage.
*   A secure link to the PDF and proof document available for the accounting entry.
*   An immutable audit log entry detailing the creation of the accounting record.
