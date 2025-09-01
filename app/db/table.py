from pydantic import BaseModel
from enum import Enum
from db import Base, Mapped, mapped_column

class RestaurantTable(Base):
    number: Mapped[int] = mapped_column()
    rid: Mapped[int] = mapped_column() # restaurant id
    status: Mapped[str] = mapped_column() # available, reserved

class RestaurantTableSchema(BaseModel):
    number: int
    rid: int

class TableStatus(str, Enum):
    available = "available"
    reserved = "reserved"
