from db import (
    BaseModel,
    Optional,
    ClassVar,
    Union,
    List,
    get_db,
    row_to_model
)

class Panorama(BaseModel):
    id: Optional[int] = None
    photo: str
    rid: int

    CREATE: ClassVar[str] = """
        CREATE TABLE IF NOT EXISTS panoramas (
            id INTEGER PRIMARY KEY,
            photo TEXT NOT NULL,
            rid INTEGER NOT NULL
        );
    """

async def db_add_panorama(
    photo: str, 
    rid: int,
) -> None:
    async with get_db() as db:
        await db.execute("""
            INSERT INTO panoramas (
                photo, 
                rid
            ) VALUES (?, ?)""", (
            photo, 
            rid,
        ))
        await db.commit()

async def db_delete_panorama(id: int):
    async with get_db() as db:
        await db.execute("DELETE FROM panoramas WHERE id = ?", (id,))
        await db.commit()
