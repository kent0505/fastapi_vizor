from db import Base, Mapped, mapped_column

class User(Base):
    phone: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=True) # admin, stuff, user
    code: Mapped[str] = mapped_column(nullable=True)
    fcm: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)
