from fastapi import UploadFile, HTTPException
from mypy_boto3_s3 import S3Client
from core.config import settings

import boto3

class S3Service:
    def __init__(self):
        self.s3: S3Client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region_name,
        )
        self.bucket = settings.s3_bucket
        self.allowed_formats = settings.image_formats
    
    async def put_object(
        self, 
        name: str, 
        file: UploadFile,
    ) -> str:
        try:
            ext = file.filename.split(".")[-1].lower()
            if ext not in self.allowed_formats:
                raise HTTPException(400, "unsupported file format")

            key = f"{name}.{ext}"
            body = await file.read()

            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=body,
                ContentType=file.content_type,
            )
            return key
        except Exception as e:
            raise HTTPException(500, str(e))

    async def delete_object(
        self, 
        key: str,
    ):
        try:
            self.s3.delete_object(
                Bucket=self.bucket,
                Key=key,
            )
        except Exception as e:
            raise HTTPException(500, str(e))

s3_service = S3Service()
