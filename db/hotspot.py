from db import Base, Mapped, mapped_column

class Hotspot(Base):
    number: Mapped[int] = mapped_column()
    latlon: Mapped[str] = mapped_column()
    pid: Mapped[int] = mapped_column()
