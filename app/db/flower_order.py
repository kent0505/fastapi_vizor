from db import Base, Mapped, mapped_column

class FlowerOrder(Base):
    uid: Mapped[int] = mapped_column() # user id
    fid: Mapped[int] = mapped_column() # flower id
    lat: Mapped[str] = mapped_column()
    lon: Mapped[str] = mapped_column()
    date: Mapped[int] = mapped_column() # timestamp
    status: Mapped[str] = mapped_column() # active, process, done
