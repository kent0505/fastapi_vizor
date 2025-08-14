from db import (
    Base, 
    Mapped, 
    AsyncSession,
    List,
    select,
    mapped_column,
)

class Hotspot(Base):
    number: Mapped[int] = mapped_column()
    latlon: Mapped[str] = mapped_column()
    pid: Mapped[int] = mapped_column()

async def db_get_hotspots(db: AsyncSession) -> List[Hotspot]:
    hotspots = await db.scalars(select(Hotspot))
    return list(hotspots)

async def db_get_hotspot_by_id(
    db: AsyncSession, 
    id: int,
) -> Hotspot | None:
    hotspot = await db.scalar(select(Hotspot).filter_by(id=id))
    return hotspot

async def db_add_hotspot(
    db: AsyncSession, 
    hotspot: Hotspot,
) -> None:
    db.add(hotspot)
    await db.commit()

async def db_delete_hotspot(
    db: AsyncSession, 
    hotspot: Hotspot,
) -> None:
    await db.delete(hotspot)
    await db.commit()
