from pydantic import BaseModel
from enum import Enum
from db import Base, Mapped, mapped_column

class FlowerOrderStatus(str, Enum):
    active = "active"
    process = "process"
    done = "done"
    cancel = "cancel"

class FlowerOrder(Base):
    uid: Mapped[int] = mapped_column() # user id
    fid: Mapped[int] = mapped_column() # flower id
    lat: Mapped[str] = mapped_column()
    lon: Mapped[str] = mapped_column()
    date: Mapped[int] = mapped_column() # timestamp
    note: Mapped[str] = mapped_column()
    message: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default=FlowerOrderStatus.active.value) # active, process, done, cancel

class FlowerOrderSchema(BaseModel):
    fid: int
    lat: str
    lon: str
    note: str
