from db import (
    BaseModel,
    Optional,
)

class Hotspot(BaseModel):
    id: Optional[int] = None
    number: int
    latlon: str
    pid: int

# async def db_add_hotspot(hotspot: Hotspot) -> None:
#     async with get_db() as db:
#         await db.execute("""
#             INSERT INTO hotspots (
#                 number, 
#                 latlon,
#                 pid
#             ) VALUES (?, ?, ?)""", (
#             hotspot.number, 
#             hotspot.latlon,
#             hotspot.pid,
#         ))
#         await db.commit()

# async def db_update_hotspot(hotspot: Hotspot) -> None:
#     async with get_db() as db:
#         await db.execute("""
#             UPDATE hotspots SET 
#                 number = ?, 
#                 latlon = ?, 
#                 pid = ?
#             WHERE id = ?""", (
#             hotspot.number,
#             hotspot.latlon,
#             hotspot.pid,
#             hotspot.id,
#         ))
#         await db.commit()

# async def db_delete_hotspot(id: int):
#     async with get_db() as db:
#         await db.execute("DELETE FROM hotspots WHERE id = ?", (id,))
#         await db.commit()
