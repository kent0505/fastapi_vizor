from db import Base, Mapped, mapped_column

class City(Base):
    name: Mapped[str] = mapped_column(unique=True)
