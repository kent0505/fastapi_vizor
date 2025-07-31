from core.db import *

class Restaurant(BaseModel):
    id: Optional[int] = None
    title: str
    type: str
    photo: Optional[str] = None
    phone: str
    instagram: str
    address: str
    latlon: str
    hours: str
    position: int

    CREATE: ClassVar[str] = """
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            photo TEXT NOT NULL DEFAULT '',
            phone TEXT NOT NULL,
            instagram TEXT NOT NULL,
            address TEXT NOT NULL,
            latlon TEXT NOT NULL,
            hours TEXT NOT NULL,
            position INTEGER NOT NULL
        );
    """

async def db_get_restaurant_by_id(id: int) -> Union[Restaurant, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM restaurants WHERE id = ?", (id,))
        row = await cursor.fetchone()
        return row_to_model(Restaurant, row)

async def db_add_restaurant(restaurant: Restaurant) -> None:
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO restaurants (
                title, 
                type, 
                phone, 
                instagram, 
                address, 
                latlon,
                hours, 
                position
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
            restaurant.title,
            restaurant.type,
            restaurant.phone,
            restaurant.instagram,
            restaurant.address,
            restaurant.latlon,
            restaurant.hours,
            restaurant.position,
        ))
        await db.commit()

async def db_update_restaurant(restaurant: Restaurant) -> None:
    async with get_db() as db:
        await db.execute(f"""
            UPDATE restaurants SET 
                title = ?, 
                type = ?, 
                phone = ?, 
                instagram = ?, 
                address = ?, 
                latlon = ?, 
                hours = ?, 
                position = ? 
            WHERE id = ?""", (
            restaurant.title,
            restaurant.type,
            restaurant.phone,
            restaurant.instagram,
            restaurant.address,
            restaurant.latlon,
            restaurant.hours,
            restaurant.position,
            restaurant.id,
        ))
        await db.commit()