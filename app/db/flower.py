from db import Base, Mapped, mapped_column

class Flower(Base):
    title: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()
    photo: Mapped[str] = mapped_column(nullable=True)
