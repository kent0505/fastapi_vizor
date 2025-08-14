from db import (
    Base, 
    Mapped, 
    AsyncSession,
    List,
    select,
    mapped_column,
)

# class Menu(Base):
#     name: Mapped[str] = mapped_column()
#     price: Mapped[str] = mapped_column()
#     currency: Mapped[str] = mapped_column()

#     photo: Mapped[str] = mapped_column()

# async def db_get_restaurants(db: AsyncSession) -> List[Restaurant]:
#     restaurants = await db.scalars(select(Restaurant))
#     return list(restaurants)

# async def db_get_restaurants_by_city(
#     db: AsyncSession, 
#     city: int,
# ) -> List[Restaurant]:
#     restaurants = await db.scalars(select(Restaurant).filter_by(city=city))
#     return list(restaurants)

# async def db_get_restaurant_by_id(
#     db: AsyncSession, 
#     id: int,
# ) -> Restaurant | None:
#     restaurant = await db.scalar(select(Restaurant).filter_by(id=id))
#     return restaurant

# async def db_add_restaurant(
#     db: AsyncSession, 
#     restaurant: Restaurant,
# ) -> None:
#     db.add(restaurant)
#     await db.commit()

# async def db_delete_restaurant(
#     db: AsyncSession, 
#     restaurant: Restaurant,
# ) -> None:
#     await db.delete(restaurant)
#     await db.commit()
