
import boto3
from config.settings import settings


def get_minio_client():
    s3_endpoint = settings.S3_ENDPOINT
    minio_username = settings.MINIO_USERNAME
    minio_key = settings.MINIO_KEY
    minio_region = settings.MINIO_REGION

    s3 = boto3.client('s3',
                      endpoint_url=s3_endpoint,
                      aws_access_key_id=minio_username,
                      aws_secret_access_key=minio_key,
                      region_name=minio_region,
                      use_ssl=False)
    return s3
