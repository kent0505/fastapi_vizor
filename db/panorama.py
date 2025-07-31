from core.db import *

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

async def db_add_panorama(photo: str, rid: int) -> None:
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO panoramas (
                photo, 
                rid
            ) VALUES (?, ?)""", (
            photo, 
            rid,
        ))
        await db.commit()
