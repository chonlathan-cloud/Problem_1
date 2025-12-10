from google.cloud import storage
from backend.src.config import settings

class GCSClient:
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = settings.GCS_BUCKET_NAME

    def upload_file(self, file_content: bytes, destination_blob_name: str, content_type: str = "application/octet-stream") -> str:
        """Uploads a file to the GCS bucket and returns its public URL."""
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(file_content, content_type=content_type)
        return blob.public_url
