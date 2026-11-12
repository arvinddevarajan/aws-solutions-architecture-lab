
import boto3
from botocore.config import Config

from config import (
    AWS_REGION,
    S3_BUCKET,
    S3_OBJECT_KEY,
    PRESIGNED_URL_EXPIRY,
)


def main():
    session = boto3.Session(region_name=AWS_REGION)
    s3 = session.client(
    "s3",
    endpoint_url="https://s3.us-east-2.amazonaws.com",
    config=Config(
        region_name="us-east-2",
        signature_version="s3v4",
        s3={"addressing_style": "path"},
    ),
)

    # s3 = session.client(
    #     "s3",
    #     config=Config(
    #         region_name=AWS_REGION,
    #         signature_version="s3v4",
    #     ),
    # )

    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": S3_OBJECT_KEY,
        },
        ExpiresIn=PRESIGNED_URL_EXPIRY,
    )

    print("Presigned URL generated successfully.")
    print("Do not share or commit this URL.")
    print(url)


if __name__ == "__main__":
    main()
