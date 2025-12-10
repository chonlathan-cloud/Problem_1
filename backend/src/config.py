import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME")

settings = Settings()
