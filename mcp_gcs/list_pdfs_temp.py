import os
import sys
from google.cloud import storage

# Assuming gcs_client.py is in the same directory
import gcs_client

if __name__ == "__main__":
    print(f"Using bucket: {gcs_client.BUCKET_NAME}")
    pdf_files = gcs_client.list_pdfs(prefix="")
    if pdf_files:
        print("PDF files in bucket:")
        for pdf in pdf_files:
            print(f"  Name: {pdf['name']}, Size: {pdf['size']}, Updated: {pdf['updated']}")
    else:
        print("No PDF files found in the bucket.")
