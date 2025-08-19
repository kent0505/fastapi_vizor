from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from pydantic import BaseModel
from typing import Annotated, Optional
from core.config import settings

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

class DatabaseHelper:
    def __init__(self):
        self.engine = create_async_engine(
            # url="sqlite+aiosqlite:///sqlite.db", 
            # echo=False,
            url=settings.db_url,
            echo=True,
        )
        self.session = async_sessionmaker(
            bind=self.engine, 
            autoflush=False, 
            expire_on_commit=False,
        )
    
    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def dispose(self):
        await self.engine.dispose()

    async def get_db(self):
        async with self.session() as session:
            yield session

db_helper = DatabaseHelper()

SessionDep = Annotated[AsyncSession, Depends(db_helper.get_db)]
