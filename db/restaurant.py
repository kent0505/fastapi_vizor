from db import (
    BaseModel,
    Optional,
    ClassVar,
    Union,
    List,
    aiosqlite,
    get_db,
    row_to_model,
)

class Restaurant(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latlon: Optional[str] = None
    hours: Optional[str] = None
    position: Optional[int] = None
    status: Optional[int] = None
    city: Optional[int] = None

    CREATE: ClassVar[str] = """
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY,
            title TEXT,
            phone TEXT,
            address TEXT,
            latlon TEXT,
            hours TEXT,
            position INTEGER,
            status INTEGER,
            city INTEGER
        );
    """

async def db_get_restaurants() -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM restaurants")
        rows = await cursor.fetchall()
        return rows

async def db_get_restaurants_by_city(city: int) -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM restaurants WHERE city = ?", (city,))
        rows = await cursor.fetchall()
        return rows

async def db_get_restaurant_by_id(id: int) -> Union[Restaurant, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM restaurants WHERE id = ?", (id,))
        row = await cursor.fetchone()
        return row_to_model(Restaurant, row)

async def db_add_restaurant(restaurant: Restaurant) -> None:
    async with get_db() as db:
        await db.execute("""
            INSERT INTO restaurants (
                title, 
                phone, 
                address,
                latlon,
                hours, 
                position,
                status,
                city
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
            restaurant.title,
            restaurant.phone,
            restaurant.address,
            restaurant.latlon,
            restaurant.hours,
            restaurant.position,
            restaurant.status,
            restaurant.city,
        ))
        await db.commit()

async def db_update_restaurant(restaurant: Restaurant) -> None:
    async with get_db() as db:
        await db.execute("""
            UPDATE restaurants SET 
                title = ?, 
                phone = ?, 
                address = ?, 
                latlon = ?, 
                hours = ?, 
                position = ?,
                status = ?,
                city = ? 
            WHERE id = ?""", (
            restaurant.title,
            restaurant.phone,
            restaurant.address,
            restaurant.latlon,
            restaurant.hours,
            restaurant.position,
            restaurant.status,
            restaurant.city,
            restaurant.id,
        ))
        await db.commit()

async def db_delete_restaurant(id: int):
    async with get_db() as db:
        await db.execute("DELETE FROM restaurants WHERE id = ?", (id,))
        await db.commit()
