from dotenv import load_dotenv
from pydantic import BaseModel

import os

load_dotenv()

class Settings(BaseModel):
    token: str = os.getenv("TOKEN")
    rabbit_url: str = os.getenv("RABBIT_URL")

settings = Settings()
