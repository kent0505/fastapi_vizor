from fastapi import UploadFile, HTTPException
from mypy_boto3_s3 import S3Client
from core.settings import settings

import boto3

s3: S3Client = boto3.client(
    "s3",
    endpoint_url=settings.endpoint_url,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name="ru-1",
)

async def delete_object(key: str):
    try:
        s3.delete_object(
            Bucket=settings.bucket, 
            Key=key,
        )
    except Exception as e:
        raise HTTPException(500, f"Failed to delete file: {str(e)}")

async def put_object(key: str, file: UploadFile):
    try:
        s3.put_object(
            Bucket=settings.bucket,
            Key=key,
            Body=await file.read(),
            ContentType=file.content_type,
        )
    except Exception as e:
        raise HTTPException(500, f"Failed to upload file: {str(e)}")
