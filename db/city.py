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

class City(BaseModel):
    id: Optional[int] = None
    name: str

    CREATE: ClassVar[str] = """
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    """

async def db_get_cities() -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM cities")
        rows = await cursor.fetchall()
        return rows

async def db_get_city_by_id(id: int) -> Union[City, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM cities WHERE id = ?", (id,))
        row = await cursor.fetchone()
        return row_to_model(City, row)

async def db_add_city(city: City) -> None:
    async with get_db() as db:
        await db.execute("INSERT INTO cities (name) VALUES (?)", (city.name,))
        await db.commit()

async def db_update_city(city: City) -> None:
    async with get_db() as db:
        await db.execute("UPDATE cities SET name = ? WHERE id = ?""", (city.name, city.id))
        await db.commit()

async def db_delete_city(id: int):
    async with get_db() as db:
        await db.execute("DELETE FROM cities WHERE id = ?", (id,))
        await db.commit()
