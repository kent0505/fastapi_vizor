from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator, Union, List
from core.schemas import (
    User, 
    Restaurant,
    Panorama,
)

import aiosqlite

@asynccontextmanager
async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    db = await aiosqlite.connect("sqlite.db")
    db.row_factory = aiosqlite.Row  # To return dict-like rows
    try:
        yield db
    finally:
        await db.close()

ID = "id INTEGER PRIMARY KEY"
TEXT = "TEXT NOT NULL"
INTEGER = "INTEGER NOT NULL"

@dataclass
class Sql:
    users: str = f"""
        CREATE TABLE IF NOT EXISTS users (
            {ID},
            name {TEXT},
            phone {TEXT},
            age {INTEGER},
            photo {TEXT} DEFAULT ''
        );
    """
    restaurants: str = f"""
        CREATE TABLE IF NOT EXISTS restaurants (
            {ID},
            title {TEXT},
            type {TEXT},
            photo {TEXT} DEFAULT '',
            phone {TEXT},
            instagram {TEXT},
            address {TEXT},
            latlon {TEXT},
            hours {TEXT},
            position {INTEGER}
        );
    """
    panoramas: str = f"""
        CREATE TABLE IF NOT EXISTS panoramas (
            {ID},
            photo {TEXT},
            rid {INTEGER}
        );
    """
    hotspots: str = f"""
        CREATE TABLE IF NOT EXISTS hotspots (
            {ID},
            number {INTEGER},
            latlon {TEXT},
            pid {INTEGER}
        );
    """
    reserves: str = f"""
        CREATE TABLE IF NOT EXISTS reserves (
            {ID},
            uid {INTEGER},
            rid {INTEGER},
            number {INTEGER},
            time {INTEGER},
            date {INTEGER},
            status {TEXT},
            note {TEXT}
        );
    """

async def db_get_users() -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        return rows

async def db_get_user_by_id(id: int) -> Union[User, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if row:
            return User(
                id=row["id"],
                name=row["name"],
                phone=row["phone"],
                age=row["age"],
                photo=row["photo"],
            )
        return row

async def db_get_user_by_phone(phone: str) -> Union[User, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM users WHERE phone = ?", (phone,))
        row = await cursor.fetchone()
        if row:
            return User(
                id=row["id"],
                name=row["name"],
                phone=row["phone"],
                age=row["age"],
                photo=row["photo"],
            )
        return row

async def db_add_user(user: User) -> None:
    async with get_db() as db:
        await db.execute("""
            INSERT INTO users (
                name, 
                phone, 
                age
            ) VALUES (?, ?, ?)""", (
            user.name, 
            user.phone, 
            user.age,
        ))
        await db.commit()

async def db_update_user(user: User) -> None:
    async with get_db() as db:
        await db.execute("""
            UPDATE users SET 
                name = ?, 
                phone = ?, 
                age = ? 
            WHERE id = ?""", (
            user.name,
            user.phone,
            user.age,
            user.id,
        ))
        await db.commit()

async def db_update_user_photo(url: str, id: int) -> None:
    async with get_db() as db:
        await db.execute("UPDATE users SET photo = ? WHERE id = ?", (url, id))
        await db.commit()

async def db_delete_user(id: int) -> None:
    async with get_db() as db:
        await db.execute("DELETE FROM users WHERE id = ?", (id,))
        await db.commit()

async def db_get_restaurants() -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM restaurants")
        rows = await cursor.fetchall()
        return rows
    
async def db_get_restaurant_by_id(id: int) -> Union[Restaurant, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM restaurants WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if row:
            return Restaurant(
                id=row["id"],
                title=row["title"],
                type=row["type"],
                photo=row["photo"],
                phone=row["phone"],
                instagram=row["instagram"],
                address=row["address"],
                latlon=row["latlon"],
                hours=row["hours"],
                position=row["position"],
            )
        return row

async def db_add_restaurant(restaurant: Restaurant) -> None:
    async with get_db() as db:
        await db.execute("""
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
        await db.execute("""
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

async def db_delete_restaurant(id: int) -> None:
    async with get_db() as db:
        await db.execute("DELETE FROM restaurants WHERE id = ?", (id,))
        await db.commit()

async def db_update_restaurant_photo(url: str, id: int) -> None:
    async with get_db() as db:
        await db.execute("UPDATE restaurants SET photo = ? WHERE id = ?", (url, id))
        await db.commit()

async def db_get_panoramas() -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM panoramas")
        rows = await cursor.fetchall()
        return rows

async def db_get_panoramas_by_rid(rid: int) -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM panoramas WHERE rid = ?", (rid,))
        rows = await cursor.fetchall()
        return rows

async def db_get_panorama_by_id(id: int) -> Union[Panorama, None]:
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM panoramas WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if row:
            return Panorama(
                id=row["id"],
                photo=row["photo"],
                rid=row["rid"],
            )
        return row

async def db_add_panorama(photo: str, rid: int) -> None:
    async with get_db() as db:
        await db.execute("""
            INSERT INTO panoramas (
                photo, 
                rid
            ) VALUES (?, ?)""", (
            photo, 
            rid,
        ))
        await db.commit()

async def db_delete_panorama(id: int) -> None:
    async with get_db() as db:
        await db.execute("DELETE FROM panoramas WHERE id = ?", (id,))
        await db.commit()
