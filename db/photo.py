from core.db import (
    get_db,
)

async def db_update_user_photo(
    photo: str, 
    id: int,
):
    async with get_db() as db:
        await db.execute("UPDATE users SET photo = ? WHERE id = ?", (photo, id))
        await db.commit()
