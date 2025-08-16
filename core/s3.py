from fastapi import UploadFile, HTTPException
from mypy_boto3_s3 import S3Client
from core.config import settings

import boto3

s3: S3Client = boto3.client(
    "s3",
    endpoint_url=settings.s3_endpoint_url,
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    region_name=settings.s3_region_name,
)

async def delete_object(key: str):
    try:
        s3.delete_object(
            Bucket=settings.s3_bucket, 
            Key=key,
        )
    except Exception as e:
        raise HTTPException(500, f"Failed to delete file: {str(e)}")

async def put_object(
    name: str, 
    file: UploadFile,
) -> str:  
    try:
        format = file.filename.split('.')[-1]
        if format not in settings.image_formats:
            raise HTTPException(400, 'file error')
        
        key = f"{name}.{format}"
    
        s3.put_object(
            Bucket=settings.s3_bucket,
            Key=key,
            Body=await file.read(),
            ContentType=file.content_type,
        )
        return key
    except Exception as e:
        raise HTTPException(500, f"Failed to upload file: {str(e)}")
