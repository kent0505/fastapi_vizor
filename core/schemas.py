from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    name: str
    phone: str
    age: int
    photo: Optional[str] = None

class Restaurant(BaseModel):
    id: Optional[int] = None
    title: str
    type: str
    photo: Optional[str] = None
    phone: str
    instagram: str
    address: str
    latlon: str
    hours: str
    position: int

class Panorama(BaseModel):
    id: Optional[int] = None
    url: str
    rid: int
