from db import (
    Base, 
    Mapped, 
    AsyncSession,
    List,
    select,
    mapped_column,
)

class Panorama(Base):
    rid: Mapped[int] = mapped_column()
    photo: Mapped[str] = mapped_column()

async def db_get_panoramas(db: AsyncSession) -> List[Panorama]:
    panoramas = await db.scalars(select(Panorama))
    return list(panoramas)

async def db_get_panoramas_by_rid(
    db: AsyncSession,
    rid: int,
) -> List[Panorama]:
    panoramas = await db.scalars(select(Panorama).filter_by(rid=rid))
    return list(panoramas)

async def db_get_panorama_by_id(
    db: AsyncSession, 
    id: int,
) -> Panorama | None:
    panorama = await db.scalar(select(Panorama).filter_by(id=id))
    return panorama
