from db import Base, Mapped, mapped_column

class User(Base):
    phone: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=True)
    code: Mapped[str] = mapped_column(nullable=True)
    chat_id: Mapped[int] = mapped_column(nullable=True)
    fcm: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)
