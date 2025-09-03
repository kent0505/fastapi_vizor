from pydantic import BaseModel
from db import Base, Mapped, mapped_column

class Flower(Base):
    title: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()
    currency: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column()

class FlowerSchema(BaseModel):
    title: str
    price: str
    currency: str
