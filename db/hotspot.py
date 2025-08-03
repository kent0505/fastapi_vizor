from db import *

class Hotspot(BaseModel):
    id: Optional[int] = None
    number: int
    latlon: str
    pid: int

    CREATE: ClassVar[str] = """
        CREATE TABLE IF NOT EXISTS hotspots (
            id INTEGER PRIMARY KEY,
            number INTEGER NOT NULL,
            latlon TEXT NOT NULL,
            pid INTEGER NOT NULL
        );
    """

async def db_add_hotspot(hotspot: Hotspot) -> None:
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO hotspots (
                number, 
                latlon,
                pid
            ) VALUES (?, ?, ?)""", (
            hotspot.number, 
            hotspot.latlon,
            hotspot.pid,
        ))
        await db.commit()

async def db_update_hotspot(hotspot: Hotspot) -> None:
    async with get_db() as db:
        await db.execute(f"""
            UPDATE hotspots SET 
                number = ?, 
                latlon = ?, 
                pid = ?
            WHERE id = ?""", (
            hotspot.number,
            hotspot.latlon,
            hotspot.pid,
            hotspot.id,
        ))
        await db.commit()
