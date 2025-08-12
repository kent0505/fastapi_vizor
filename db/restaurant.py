from db import (
    Base, 
    Mapped, 
    BaseModel,
    AsyncSession,
    List,
    Optional,
    select,
    mapped_column,
)

class RestaurantBody(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latlon: Optional[str] = None
    hours: Optional[str] = None
    position: Optional[int] = None
    city: Optional[int] = None
    status: Optional[int] = None

class Restaurant(Base):
    title: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    latlon: Mapped[str] = mapped_column()
    hours: Mapped[str] = mapped_column()
    position: Mapped[int] = mapped_column()
    city: Mapped[int] = mapped_column()
    status: Mapped[int] = mapped_column()
    photo: Mapped[str] = mapped_column()

async def db_get_restaurants(db: AsyncSession) -> List[Restaurant]:
    restaurants = await db.scalars(select(Restaurant))
    return list(restaurants)

async def db_get_restaurants_by_city(
    db: AsyncSession, 
    city: int,
) -> List[Restaurant]:
    restaurants = await db.scalars(select(Restaurant).filter_by(city=city))
    return list(restaurants)

async def db_get_restaurant_by_id(
    db: AsyncSession, 
    id: int,
) -> Restaurant | None:
    restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
    return restaurant

async def db_add_restaurant(
    db: AsyncSession, 
    restaurant: Restaurant,
) -> None:
    db.add(restaurant)
    await db.commit()

async def db_delete_restaurant(
    db: AsyncSession, 
    restaurant: Restaurant,
):
    await db.delete(restaurant)
    await db.commit()
