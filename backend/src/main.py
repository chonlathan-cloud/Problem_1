import logging
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from backend.src.api import accounting_entry_router
from backend.src.api import auth_router
from backend.src.database import init_db
from backend.src.utils.error_handler import http_exception_handler, generic_exception_handler
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Accounting Entry API",
    description="API for managing accounting entries, including creation, PDF generation, and GCS upload.",
    version="1.0.0"
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Application startup complete.")

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(accounting_entry_router.router, prefix="/api/v1")

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
