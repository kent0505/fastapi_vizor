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
