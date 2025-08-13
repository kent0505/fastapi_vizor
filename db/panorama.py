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

async def db_get_panorama_by_id(
    db: AsyncSession, 
    id: int,
) -> Panorama | None:
    panorama = await db.scalar(select(Panorama).filter_by(id=id))
    return panorama

async def db_add_panorama(
    db: AsyncSession, 
    panorama: Panorama,
) -> None:
    db.add(panorama)
    await db.commit()

async def db_delete_panorama(
    db: AsyncSession, 
    panorama: Panorama,
) -> None:
    await db.delete(panorama)
    await db.commit()
