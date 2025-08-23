from db import Base, Mapped, mapped_column
from enum import Enum

class RestaurantTable(Base):
    number: Mapped[int] = mapped_column()
    rid: Mapped[int] = mapped_column() # restaurant id
    status: Mapped[str] = mapped_column() # available, reserved

class TableStatus(str, Enum):
    available = "available"
    reserved = "reserved"
