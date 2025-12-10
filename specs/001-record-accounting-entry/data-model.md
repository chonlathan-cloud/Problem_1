# Data Model: Record Accounting Entry and Generate PDF

This document outlines the data entities and their relationships for the "Record Accounting Entry and Generate PDF" feature, based on the functional requirements and key entities defined in the feature specification.

## Entities

### 1. AccountingEntry

Represents a single daily financial record input by an employee.

**Attributes**:

-   `id`: Unique identifier for the accounting entry (Primary Key, auto-generated).
-   `date`: The date of the accounting entry (Date, mandatory).
    -   *Validation*: Must not be in the future.
-   `document_type`: The type of document (String, mandatory).
-   `description`: A description of the entry (Text, mandatory).
-   `amount`: The monetary amount of the entry (Decimal, mandatory).
    -   *Validation*: Must be greater than 0.
-   `vat`: The Value Added Tax percentage (Decimal, mandatory).
    -   *Validation*: Must be between 0 and 7 (inclusive).
-   `recorder_id`: Identifier of the employee who recorded the entry (Foreign Key to User entity, mandatory).
-   `remarks`: Additional remarks or notes (Text, optional).
-   `proof_attachment_link`: URL or path to the attached proof document (String, optional).
-   `pdf_unique_ref_number`: A unique reference number for the generated PDF (String, auto-generated).
-   `gcs_pdf_link`: URL to the generated PDF uploaded to Google Cloud Storage (String).
-   `created_at`: Timestamp when the entry was created (Datetime, auto-generated).
-   `updated_at`: Timestamp when the entry was last updated (Datetime, auto-generated).

**Relationships**:

-   `recorder_id` links to a `User` entity (implicitly, as the Recorder is an employee).

### 2. AuditLogEntry

Records system activities related to the creation and modification of accounting entries.

**Attributes**:

-   `id`: Unique identifier for the audit log entry (Primary Key, auto-generated).
-   `timestamp`: The exact time when the event occurred (Datetime, auto-generated).
-   `user_id`: Identifier of the user who performed the action (Foreign Key to User entity, mandatory).
-   `action_type`: Type of action performed (e.g., 'ENTRY_CREATED', 'ENTRY_UPDATED') (String, mandatory).
-   `target_entry_id`: Identifier of the `AccountingEntry` that was affected (Foreign Key to AccountingEntry, mandatory).
-   `details_of_change`: JSON or Text field containing details of the change (e.g., old and new values for updated fields) (Text/JSON, optional).

**Relationships**:

-   `user_id` links to a `User` entity.
-   `target_entry_id` links to an `AccountingEntry` entity.

**Behavior**: Append-only format; existing audit log entries cannot be modified or deleted.
