from pydantic import BaseModel
from enum import Enum
from db import Base, Mapped, mapped_column

class RestaurantStatus(str, Enum):
    active = "active"
    disabled = "disabled"

class Restaurant(Base):
    title: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    lat: Mapped[str] = mapped_column()
    lon: Mapped[str] = mapped_column()
    hours: Mapped[str] = mapped_column()
    city: Mapped[int] = mapped_column() # city id
    position: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(default=RestaurantStatus.active.value)
    photo: Mapped[str] = mapped_column()

class RestaurantSchema(BaseModel):
    title: str
    phone: str
    address: str
    lat: str
    lon: str
    hours: str
    city: int
