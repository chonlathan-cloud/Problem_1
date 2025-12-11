gcs_list_pdfs
prefix: string – เช่น "pdfs/2025/12/"
limit: int – จำนวนสูงสุด (เช่น default 20)
{
  "items": [
    {
      "name": "pdfs/2025/12/entry-123.pdf",
      "size": 12345,
      "updated": "2025-12-10T10:00:00Z"
    }
  ]
}

gcs_get_pdf_metadata
input path: string – เช่น "pdfs/2025/12/entry-123.pdf"
output: 
{
  "name": "pdfs/2025/12/entry-123.pdf",
  "size": 12345,
  "contentType": "application/pdf",
  "updated": "2025-12-10T10:00:00Z",
  "crc32c": "xxxx",
  "md5Hash": "yyyy"
}

gcs_get_signed_url
input path: string – เช่น "pdfs/2025/12/entry-123.pdf"
output 
{
  "url": "https://storage.googleapis.com/...",
  "expiresAt": "2025-12-10T10:30:00Z"
}

