import requests
import base64
import json

# Create dummy PDF content
pdf_content = b"dummy pdf content"
pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

url = "http://localhost:8000/api/v1/accounting-entries"
headers = {
    "Authorization": "Bearer mock_jwt_token",
    "Content-Type": "application/json"
}
payload = {
    "date": "2023-10-27",
    "document_type": "Invoice",
    "description": "Office Supplies",
    "amount": 100.00,
    "vat": 7.00,
    "recorder_id": "EMP001",
    "remarks": "Test entry via script",
    "attach_proof_base64": pdf_base64
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
