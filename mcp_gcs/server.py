import sys
import json
from mcp_gcs.gcs_client import list_pdfs, get_pdf_metadata, get_signed_url

def handle_request(rep: dict) -> dict:
    method = rep.get("method")
    params = rep.get("params",{}) or {}

    if method == "gcs_list_pdfs":
        item = list_pdfs(
            prefix=params.get("prefix", ""),
            limit=params.get("limit", 20),
        )
        return {"result":{"item":item}}
    if method == "gcs_get_pdf_metadata":
        meta = get_pdf_metadata(params["path"])
        return {"result":meta}
    
    if method == "gcs_get_signed_url":
        data = get_signed_url(
            path=params["path"],
            expires_in_minutes=params.get("expires_in_minutes", 10),
        )
        return {"result":data}
    #Unknown method
    return {"error":{"code":-32601,"message":"Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        req = json.loads(line)
        resp = handle_request(req)
        # attach id vack if present
        if "id" in req:
            resp["id"] = req["id"]
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
