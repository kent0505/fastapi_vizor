from db import Base, Mapped, mapped_column

class Panorama(Base):
    rid: Mapped[int] = mapped_column()
    photo: Mapped[str] = mapped_column()
