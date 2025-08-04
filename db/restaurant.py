from db import (
    BaseModel,
    Optional,
    ClassVar,
    Union,
    get_db,
    row_to_model,
)

class Restaurant(BaseModel):
    id: Optional[int] = None
    title: str
    type: str
    phone: str
    instagram: str
    address: str
    latlon: str
    hours: str
    position: int
    status: int
    city: int

    CREATE: ClassVar[str] = """
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            phone TEXT NOT NULL,
            instagram TEXT NOT NULL,
            address TEXT NOT NULL,
            latlon TEXT NOT NULL,
            hours TEXT NOT NULL,
            position INTEGER NOT NULL,
            status INTEGER NOT NULL,
            city INTEGER NOT NULL
        );
    """

async def db_get_restaurant_by_id(id: int) -> Union[Restaurant, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM restaurants WHERE id = ?", (id,))
        row = await cursor.fetchone()
        return row_to_model(Restaurant, row)

async def db_get_restaurant_by_city(city: str) -> Union[Restaurant, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM restaurants WHERE city = ?", (city,))
        row = await cursor.fetchone()
        return row_to_model(Restaurant, row)

async def db_add_restaurant(restaurant: Restaurant) -> None:
    async with get_db() as db:
        await db.execute("""
            INSERT INTO restaurants (
                title, 
                type, 
                phone, 
                instagram, 
                address,
                city,
                latlon,
                hours, 
                position,
                status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            restaurant.title,
            restaurant.type,
            restaurant.phone,
            restaurant.instagram,
            restaurant.address,
            restaurant.city,
            restaurant.latlon,
            restaurant.hours,
            restaurant.position,
            restaurant.status,
        ))
        await db.commit()

async def db_update_restaurant(restaurant: Restaurant) -> None:
    async with get_db() as db:
        await db.execute("""
            UPDATE restaurants SET 
                title = ?, 
                type = ?, 
                phone = ?, 
                instagram = ?, 
                address = ?, 
                city = ?,
                latlon = ?, 
                hours = ?, 
                position = ?,
                status = ?
            WHERE id = ?""", (
            restaurant.title,
            restaurant.type,
            restaurant.phone,
            restaurant.instagram,
            restaurant.address,
            restaurant.city,
            restaurant.latlon,
            restaurant.hours,
            restaurant.position,
            restaurant.status,
            restaurant.id,
        ))
        await db.commit()

async def db_delete_restaurant(id: int):
    async with get_db() as db:
        await db.execute("DELETE FROM restaurants WHERE id = ?", (id,))
        await db.commit()
