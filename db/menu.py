from db import Base, Mapped, mapped_column

class Menu(Base):
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()
    currency: Mapped[str] = mapped_column()
    cid: Mapped[int] = mapped_column() # category id
    rid: Mapped[int] = mapped_column() # restaurant id
    photo: Mapped[str] = mapped_column()
