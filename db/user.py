from db import (
    BaseModel,
    Optional,
    ClassVar,
    Union,
    List,
    get_db,
    row_to_model
)

import aiosqlite

class LoginBody(BaseModel):
    phone: str
    code: int
    password: str = ''

class User(BaseModel):
    id: Optional[int] = None
    name: str
    phone: str
    password: str
    age: int
    role: Optional[str] = None
    code: Optional[int] = None

    CREATE: ClassVar[str] = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            role TEXT NOT NULL,
            code INTEGER NOT NULL
        );
    """

async def db_get_user_by_id(id: int) -> Union[User, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = await cursor.fetchone()
        return row_to_model(User, row)

async def db_get_user_by_phone(phone: str) -> Union[User, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM users WHERE phone = ?", (phone,))
        row = await cursor.fetchone()
        return row_to_model(User, row)

async def db_get_users() -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        return rows

async def db_add_user(
    user: User,
    role: str,
):
    async with get_db() as db:
        await db.execute("""
            INSERT INTO users (
                name,
                phone,
                password,
                age,
                code,
                role
            ) VALUES (?, ?, ?, ?, ?, ?)""", (
            user.name, 
            user.phone, 
            user.password,
            user.age,
            user.code,
            role,
        ))
        await db.commit()

async def db_update_user(
    user: User,
    role: str,
) -> None:
    async with get_db() as db:
        await db.execute("""
            UPDATE users SET 
                name = ?, 
                phone = ?, 
                password = ?,
                age = ?,
                code = ?,
                role = ?
            WHERE id = ?""", (
            user.name,
            user.phone,
            user.password,
            user.age,
            user.code,
            role,
            user.id,
        ))
        await db.commit()

async def db_delete_user(id: int):
    async with get_db() as db:
        await db.execute("DELETE FROM users WHERE id = ?", (id,))
        await db.commit()
