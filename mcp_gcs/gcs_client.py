from typing import List, Dict
from google.cloud import storage
import os
from datetime import timedelta, datetime, timezone

BUCKET_NAME = os.environ.get("GCS_PDF_BUCKET", "ps1task")

storage_client = storage.Client()

def list_pdfs(prefix: str, limit: int = 20) -> List[Dict]:
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix=prefix, max_results=limit)
    items = []
    for b in blobs:
        if not b.name.lower().endswith(".pdf"):
            continue
        items.append({
            "name": b.name,
            "size": b.size,
            "updated": b.updated.isoformat() if b.updated else None,
        })
    return items

def get_pdf_metadata(path: str) -> Dict:
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(path)
    blob.reload()
    return {
        "name": blob.name,
        "size": blob.size,
        "contentType": blob.content_type,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "crc32c": blob.crc32c,
        "md5Hash": blob.md5_hash,
    }

def get_signed_url(path: str, expires_in_minutes: int) -> Dict:
    # guard TTL
    expires_in = max(1, min(expires_in_minutes, 60))

    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(path)

    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=expires_in)

    url = blob.generate_signed_url(expiration=expiration, method="GET")

    return {
        "url": url,
        "expiresAt": expiration.isoformat()
    }

print()

