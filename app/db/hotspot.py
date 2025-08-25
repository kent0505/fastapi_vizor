from db import Base, Mapped, mapped_column

class Hotspot(Base):
    lat: Mapped[str] = mapped_column()
    lon: Mapped[str] = mapped_column()
    rid: Mapped[int] = mapped_column() # restaurant id
    pid: Mapped[int] = mapped_column() # panorama id
    tid: Mapped[int] = mapped_column() # table id
