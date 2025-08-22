from db import Base, Mapped, mapped_column

class RestaurantTable(Base):
    number: Mapped[int] = mapped_column()
    rid: Mapped[int] = mapped_column() # restaurant id
    status: Mapped[str] = mapped_column()
