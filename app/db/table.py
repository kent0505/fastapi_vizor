from pydantic import BaseModel
from enum import Enum
from db import Base, Mapped, mapped_column

class TableStatus(str, Enum):
    available = "available"
    reserved = "reserved"

class RestaurantTable(Base):
    number: Mapped[int] = mapped_column()
    rid: Mapped[int] = mapped_column() # restaurant id
    status: Mapped[str] = mapped_column(default=TableStatus.available.value) # available, reserved

class RestaurantTableSchema(BaseModel):
    number: int
    rid: int
