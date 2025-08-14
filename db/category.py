from db import (
    Base, 
    Mapped, 
    AsyncSession,
    List,
    select,
    mapped_column,
)

class Category(Base):
    name: Mapped[str] = mapped_column(unique=True)

async def db_get_categories(db: AsyncSession) -> List[Category]:
    categories = await db.scalars(select(Category))
    return list(categories)

async def db_get_category_by_id(
    db: AsyncSession, 
    id: int,
) -> Category | None:
    category = await db.scalar(select(Category).filter_by(id=id))
    return category
