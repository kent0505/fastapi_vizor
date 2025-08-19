from db import Base, Mapped, mapped_column

class Category(Base):
    name: Mapped[str] = mapped_column(unique=True)
