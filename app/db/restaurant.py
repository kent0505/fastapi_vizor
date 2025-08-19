from db import Base, Mapped, mapped_column

class Restaurant(Base):
    title: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    latlon: Mapped[str] = mapped_column()
    hours: Mapped[str] = mapped_column()
    city: Mapped[int] = mapped_column()
    position: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[int] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)
