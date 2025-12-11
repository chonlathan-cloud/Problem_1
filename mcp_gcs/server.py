import sys
import json
import logging
# ปรับ import ให้ตรงกับ structure ของคุณ
# ถ้า run module แบบ python -m mcp_gcs.server อาจต้องระวังเรื่อง path
# แต่ถ้าใน env setup ไว้แล้วก็ใช้แบบเดิมได้ครับ
from mcp_gcs.gcs_client import list_pdfs, get_pdf_metadata, get_signed_url

# Setup logging เพื่อ debug ง่ายขึ้น (จะออกไปที่ stderr ไม่กวน stdout ที่ใช้ส่ง json)
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("mcp-server")

def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {}) or {}
    msg_id = req.get("id")

    logger.info(f"Received request: {method}")

    # 1. MCP Handshake: Initialize
    # Client จะส่งมาเป็นอันดับแรก เพื่อถาม Protocol version และ Capabilities
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05", # ระบุเวอร์ชัน MCP
                "capabilities": {
                    "tools": {} # บอกว่า Server นี้มีความสามารถด้าน Tools
                },
                "serverInfo": {
                    "name": "gcs-pdf-tools",
                    "version": "0.1.0"
                }
            }
        }

    # 2. MCP Notification: Initialized
    # Client ส่งมาบอกว่ารับทราบการ Initialize แล้ว (ไม่ต้องตอบกลับ result)
    if method == "notifications/initialized":
        return None # Notification ไม่ต้องมี response

    # 3. MCP Discovery: List Tools
    # Client จะเรียกเพื่อขอรายการ Tools ทั้งหมดที่ Server นี้มี
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "gcs_list_pdfs",
                        "description": "List PDF files in the GCS bucket with optional prefix filtering.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prefix": {"type": "string", "description": "Prefix filter for GCS objects (e.g., 'pdfs/2025/')"},
                                "limit": {"type": "integer", "description": "Maximum number of files to return (default 20)"}
                            },
                            "required": []
                        }
                    },
                    {
                        "name": "gcs_get_pdf_metadata",
                        "description": "Get metadata for a specific PDF file.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "Full path to the file in GCS"}
                            },
                            "required": ["path"]
                        }
                    },
                    {
                        "name": "gcs_get_signed_url",
                        "description": "Generate a signed URL for temporary access to a file.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "Full path to the file in GCS"},
                                "expires_in_minutes": {"type": "integer", "description": "Expiration time in minutes (default 10, max 60)"}
                            },
                            "required": ["path"]
                        }
                    }
                ]
            }
        }

    # 4. Tool Execution: Call Tool
    # Client ส่งคำสั่งเรียกใช้ Tool จริงๆ
    if method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        try:
            result_content = []
            
            if tool_name == "gcs_list_pdfs":
                data = list_pdfs(
                    prefix=tool_args.get("prefix", ""),
                    limit=tool_args.get("limit", 20)
                )
                result_content = [{"type": "text", "text": json.dumps(data, indent=2)}]

            elif tool_name == "gcs_get_pdf_metadata":
                data = get_pdf_metadata(path=tool_args["path"])
                result_content = [{"type": "text", "text": json.dumps(data, indent=2)}]

            elif tool_name == "gcs_get_signed_url":
                data = get_signed_url(
                    path=tool_args["path"],
                    expires_in_minutes=tool_args.get("expires_in_minutes", 10)
                )
                result_content = [{"type": "text", "text": json.dumps(data, indent=2)}]
            
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": result_content,
                    "isError": False
                }
            }
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                    "isError": True
                }
            }

    # Unknown method
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": "Method not found"}
    }

def main():
    # Loop รอรับ Input จาก Stdin (MCP สื่อสารผ่าน Stdio)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            if resp: # ถ้ามี response (notification จะเป็น None)
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            logger.error(f"Error processing line: {e}")
            # ส่ง error กลับถ้า parse json ไม่ได้
            pass

if __name__ == "__main__":
    main()