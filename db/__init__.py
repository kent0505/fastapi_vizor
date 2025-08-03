from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import AsyncGenerator, Union, Type, List, Optional, ClassVar

import aiosqlite

@asynccontextmanager
async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    db = await aiosqlite.connect("sqlite.db")
    db.row_factory = aiosqlite.Row # To return dict-like rows
    try:
        yield db
    finally:
        await db.close()

def row_to_model(
    model_class: Type[BaseModel], 
    row: Union[aiosqlite.Row, None],
) -> Union[BaseModel, None]:
    if row is None: 
        return None
    return model_class(**dict(row))
