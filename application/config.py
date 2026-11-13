
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class AppConfig:
    aws_region: str
    s3_bucket: str
    s3_object_key: str
    presigned_url_expiry: int

    @classmethod
    def from_env(cls):
        region = os.getenv("AWS_REGION", "").strip()
        bucket = os.getenv("S3_BUCKET", "").strip()
        object_key = os.getenv("S3_OBJECT_KEY", "").strip()
        expiry = os.getenv("PRESIGNED_URL_EXPIRY", "300")

        if not region:
            raise ValueError("AWS_REGION is required")

        if not bucket:
            raise ValueError("S3_BUCKET is required")

        if not object_key:
            raise ValueError("S3_OBJECT_KEY is required")

        try:
            expiry = int(expiry)
        except ValueError:
            raise ValueError(
                "PRESIGNED_URL_EXPIRY must be an integer"
            ) from None

        if not 1 <= expiry <= 3600:
            raise ValueError(
                "PRESIGNED_URL_EXPIRY must be between 1 and 3600 seconds"
            )

        return cls(
            aws_region=region,
            s3_bucket=bucket,
            s3_object_key=object_key,
            presigned_url_expiry=expiry,
        )
