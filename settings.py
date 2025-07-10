from pydantic import BaseModel

import os

class Settings(BaseModel):
    swagger: dict = {
        "defaultModelsExpandDepth": -1,
    }
    token: str = os.getenv("TOKEN")
    # url: str = os.getenv("URL")
    # otaw: int = 1093286245
    # umar: int = 507330315

settings = Settings()
