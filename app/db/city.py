from pydantic import BaseModel
from db import Base, Mapped, mapped_column

class City(Base):
    name: Mapped[str] = mapped_column(unique=True)
    position: Mapped[int] = mapped_column(default=0)

class CitySchema(BaseModel):
    name: str
