from db import (
    Base, 
    Mapped, 
    AsyncSession,
    List,
    select,
    mapped_column,
)

class Menu(Base):
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()
    currency: Mapped[str] = mapped_column()
    cid: Mapped[int] = mapped_column() # category id
    rid: Mapped[int] = mapped_column() # restaurant id
    photo: Mapped[str] = mapped_column()

async def db_get_menus(db: AsyncSession) -> List[Menu]:
    menus = await db.scalars(select(Menu))
    return list(menus)

async def db_get_menus_by_restaurant(
    db: AsyncSession, 
    rid: int,
) -> List[Menu]:
    menus = await db.scalars(select(Menu).filter_by(rid=rid))
    return list(menus)

async def db_get_menu_by_id(
    db: AsyncSession, 
    id: int,
) -> Menu | None:
    menu = await db.scalar(select(Menu).filter_by(id=id))
    return menu
