from dotenv import load_dotenv
from pydantic import BaseModel

import os

load_dotenv()

class Settings(BaseModel):
    swagger: dict = {"defaultModelsExpandDepth": -1}

    # broker
    rabbit_url: str = os.getenv("RABBIT_URL")

settings = Settings()
