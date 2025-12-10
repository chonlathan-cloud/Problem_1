from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

class PDFGenerator:
    def generate_accounting_entry_pdf(self, entry_data: dict) -> BytesIO:
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        p.drawString(100, 750, f"Accounting Entry Record")
        p.drawString(100, 730, f"Date: {entry_data.get('date')}")
        p.drawString(100, 710, f"Document Type: {entry_data.get('document_type')}")
        p.drawString(100, 690, f"Description: {entry_data.get('description')}")
        p.drawString(100, 670, f"Amount: {entry_data.get('amount')}")
        p.drawString(100, 650, f"VAT: {entry_data.get('vat')}%")
        p.drawString(100, 630, f"Recorder ID: {entry_data.get('recorder_id')}")
        p.drawString(100, 610, f"Remarks: {entry_data.get('remarks', 'N/A')}")
        p.drawString(100, 590, f"Reference Number: {entry_data.get('pdf_unique_ref_number', 'N/A')}")

        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
