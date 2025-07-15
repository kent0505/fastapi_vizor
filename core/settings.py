from pydantic import BaseModel

import os

class Settings(BaseModel):
    swagger:       dict = {"defaultModelsExpandDepth": -1}
    password:      str = os.getenv("PASSWORD")
    token:         str = os.getenv("TOKEN")
    jwt_key:       str = os.getenv("KEY", "xyz")
    day_seconds:   int = 86400
    year_seconds:  int = 31536000
    admin:         str = "admin"
    user:          str = "user"

settings = Settings()
