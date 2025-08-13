from db import (
    Base, 
    Mapped, 
    AsyncSession,
    List,
    select,
    mapped_column,
)

class City(Base):
    name: Mapped[str] = mapped_column(unique=True)

async def db_get_cities(db: AsyncSession) -> List[City]:
    cities = await db.scalars(select(City))
    return list(cities)

async def db_get_city_by_id(
    db: AsyncSession, 
    id: int,
) -> City | None:
    city = await db.scalar(select(City).filter_by(id=id))
    return city

async def db_add_city(
    db: AsyncSession, 
    city: City,
) -> None:
    db.add(city)
    await db.commit()

async def db_delete_city(
    db: AsyncSession, 
    city: City,
):
    await db.delete(city)
    await db.commit()
