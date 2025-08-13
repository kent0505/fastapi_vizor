from fastapi import Depends
from sqlalchemy import select, desc
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import Annotated, List, Optional
from pydantic import BaseModel

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

class DatabaseHelper:
    def __init__(self):
        self.engine = create_async_engine(
            url="sqlite+aiosqlite:///sqlite.db", 
            echo=False,
        )
        self.session = async_sessionmaker(
            bind=self.engine, 
            autoflush=False, 
            expire_on_commit=False,
        )
    
    async def dispose(self):
        await self.engine.dispose()

    async def get_db(self):
        async with self.session() as session:
            yield session

db_helper = DatabaseHelper()

async def create_all():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def dispose_db():
    await db_helper.dispose()

SessionDep = Annotated[AsyncSession, Depends(db_helper.get_db)]
