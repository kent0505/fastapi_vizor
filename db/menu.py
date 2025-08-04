from db import (
    BaseModel,
    Optional,
    ClassVar,
    get_db,
)

class Menu(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    category: str
    photo: Optional[str] = None
    price: str
    rid: int

    CREATE: ClassVar[str] = """
        CREATE TABLE IF NOT EXISTS menus (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            photo TEXT NOT NULL DEFAULT '',
            price TEXT NOT NULL,
            rid INTEGER NOT NULL
        );
    """

async def db_add_menu(menu: Menu) -> None:
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO menus (
                title, 
                description,
                category,
                price,
                rid
            ) VALUES (?, ?, ?, ?, ?)""", (
            menu.title, 
            menu.description,
            menu.category,
            menu.price,
            menu.rid,
        ))
        await db.commit()

async def db_update_menu(menu: Menu) -> None:
    async with get_db() as db:
        await db.execute(f"""
            UPDATE menus SET 
                title = ?, 
                description = ?, 
                category = ?,
                price = ?,
                rid = ?
            WHERE id = ?""", (
            menu.title,
            menu.description,
            menu.category,
            menu.price,
            menu.rid,
            menu.id,
        ))
        await db.commit()

async def db_delete_menu(id: int):
    async with get_db() as db:
        await db.execute("DELETE FROM menus WHERE id = ?", (id,))
        await db.commit()
