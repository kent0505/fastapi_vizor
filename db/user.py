from db import (
    Base, 
    Mapped, 
    AsyncSession,
    List,
    select,
    mapped_column,
)

class User(Base):
    phone: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=True)
    code: Mapped[str] = mapped_column(nullable=True)
    fcm: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)

async def db_get_users(db: AsyncSession) -> List[User]:
    users = await db.scalars(select(User))
    return list(users)

async def db_get_user_by_id(
    db: AsyncSession, 
    id: int,
) -> User | None:
    user = await db.scalar(select(User).filter_by(id=id))
    return user

async def db_get_user_by_phone(
    db: AsyncSession, 
    phone: str,
) -> User | None:
    user = await db.scalar(select(User).filter_by(phone=phone))
    return user

async def db_add_user(
    db: AsyncSession, 
    user: User,
) -> None:
    db.add(user)
    await db.commit()

async def db_delete_user(
    db: AsyncSession, 
    user: User,
) -> None:
    await db.delete(user)
    await db.commit()
