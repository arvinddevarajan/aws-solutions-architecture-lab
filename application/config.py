import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")

AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
S3_BUCKET = os.environ["S3_BUCKET"]
S3_OBJECT_KEY = os.getenv("S3_OBJECT_KEY", "sample.txt")
PRESIGNED_URL_EXPIRY = int(
    os.getenv("PRESIGNED_URL_EXPIRY", "300")
)
