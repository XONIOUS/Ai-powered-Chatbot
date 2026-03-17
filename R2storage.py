import boto3
import os
from botocore.config import Config
from botocore.exceptions import ClientError


def get_r2_client():
    """Create and return an R2 client."""
    return boto3.client(
        "s3",
        endpoint_url=f"https://{os.getenv('CF_ACCOUNT_ID')}.r2.cloudflarestorage.com",
        aws_access_key_id=os.getenv("CF_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("CF_SECRET_ACCESS_KEY"),
        config=Config(signature_version="s3v4"),
        region_name="auto"
    )


BUCKET = os.getenv("CF_BUCKET_NAME", "pdf-chatbot")


def upload_file_to_r2(local_path, r2_key):
    """Upload a local file to R2."""
    client = get_r2_client()
    client.upload_file(local_path, BUCKET, r2_key)
    print(f"Uploaded {local_path} to R2 as {r2_key}")


def download_file_from_r2(r2_key, local_path):
    """Download a file from R2 to local path."""
    client = get_r2_client()
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    client.download_file(BUCKET, r2_key, local_path)
    print(f"Downloaded {r2_key} from R2 to {local_path}")


def file_exists_in_r2(r2_key):
    """Check if a file exists in R2."""
    client = get_r2_client()
    try:
        client.head_object(Bucket=BUCKET, Key=r2_key)
        return True
    except ClientError:
        return False
