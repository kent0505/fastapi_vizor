from db import Base, Mapped, mapped_column

class Panorama(Base):
    rid: Mapped[int] = mapped_column() # restaurant id
    photo: Mapped[str] = mapped_column()
