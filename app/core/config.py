from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

import os

load_dotenv()

class Swagger(BaseModel):
    ui_parameters: dict = {"defaultModelsExpandDepth": -1}

class JWT(BaseModel):
    version: int = 1
    exp: int = 31536000 # one year
    key: str = os.getenv("KEY")
    algorithm: str = "HS256"
    admin: str = os.getenv("ADMIN")

class S3(BaseModel):
    endpoint_url: str = os.getenv("S3_URL")
    region_name: str = os.getenv("S3_REGION")
    access_key: str = os.getenv("S3_ACCESS_KEY")
    secret_key: str = os.getenv("S3_SECRET_KEY")
    bucket: str = os.getenv("S3_BUCKET")

class DB(BaseModel):
    url: str = os.getenv("POSTGRES_URL") # "sqlite+aiosqlite:///sqlite.db"

class Rabbit(BaseModel):
    url: str = os.getenv("RABBIT_URL")

class Twilio(BaseModel):
    account_sid: str = os.getenv("ACCOUNT_SID")
    auth_token: str = os.getenv("AUTH_TOKEN")

class Settings(BaseSettings):
    swagger: Swagger = Swagger()
    jwt: JWT = JWT()
    s3: S3 = S3()
    db: DB = DB()
    rabbit: Rabbit = Rabbit()
    twilio: Twilio = Twilio()

settings = Settings()
