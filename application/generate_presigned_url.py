
import logging
import sys

import boto3
from logger import configure_logging
from botocore.config import Config
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    LoginRefreshRequired,
    NoCredentialsError,
    PartialCredentialsError,
)

from config import AppConfig


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
configure_logging()
logger = logging.getLogger(__name__)


def generate_presigned_url(config: AppConfig) -> str:
    session = boto3.Session(region_name=config.aws_region)

    s3 = session.client(
        "s3",
        endpoint_url=f"https://s3.{config.aws_region}.amazonaws.com",
        config=Config(
            region_name=config.aws_region,
            signature_version="s3v4",
            s3={"addressing_style": "path"},
        ),
    )

    # Confirm that the object is accessible before signing.
    s3.head_object(
        Bucket=config.s3_bucket,
        Key=config.s3_object_key,
    )

    return s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": config.s3_bucket,
            "Key": config.s3_object_key,
        },
        ExpiresIn=config.presigned_url_expiry,
    )


def main():
    try:
        config = AppConfig.from_env()

        logger.info("Starting S3 presigned URL generation")

        url = generate_presigned_url(config)

        logger.info(
            "Presigned URL generated successfully; expiry=%s seconds",
            config.presigned_url_expiry,
        )

        # Lab-only: use the URL without logging it.
        # We'll add a secure delivery mechanism later.
        print("SUCCESS: Presigned URL generated")
        return 0

    except ValueError as exc:
        logger.error("Configuration error: %s", exc)
        return 1
    
    except LoginRefreshRequired:
        logger.error(
            "AWS session expired. Reauthenticate using aws login."
        )
        return 1

    except (NoCredentialsError, PartialCredentialsError):
        logger.error(
            "AWS credentials are missing or incomplete. "
            "Check your AWS profile configuration."
        )
        return 1


    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        logger.error("AWS S3 operation failed: %s", error_code)
        return 1

    except BotoCoreError:
        logger.error("AWS SDK operation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
