from db import (
    Base, 
    Mapped, 
    AsyncSession,
    List,
    select,
    mapped_column,
)

class Restaurant(Base):
    title: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    latlon: Mapped[str] = mapped_column()
    hours: Mapped[str] = mapped_column()
    city: Mapped[int] = mapped_column()
    position: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[int] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)

async def db_get_restaurants(db: AsyncSession) -> List[Restaurant]:
    restaurants = await db.scalars(select(Restaurant))
    return list(restaurants)

async def db_get_restaurants_by_city(
    db: AsyncSession, 
    city: int,
) -> List[Restaurant]:
    restaurants = await db.scalars(
        select(Restaurant)
        .filter_by(city=city)
        .order_by(Restaurant.position)
    )
    return list(restaurants)

async def db_get_restaurant_by_id(
    db: AsyncSession, 
    id: int,
) -> Restaurant | None:
    restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
    return restaurant
