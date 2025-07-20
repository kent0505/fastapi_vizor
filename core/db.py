from contextlib import asynccontextmanager
from typing import AsyncGenerator, Union, List
from core.schemas import (
    User, 
    Restaurant,
    Panorama,
    Hotspot,
    Menu,
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
        cursor = await db.execute("SELECT * FROM panoramas")
        rows = await cursor.fetchall()
        return rows

async def db_get_panoramas_by_rid(rid: int) -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM panoramas WHERE rid = ?", (rid,))
        rows = await cursor.fetchall()
        return rows

async def db_get_panorama_by_id(id: int) -> Union[Panorama, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM panoramas WHERE id = ?", (id,))
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

async def db_get_hotspots() -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM hotspots")
        rows = await cursor.fetchall()
        return rows

async def db_get_hotspots_by_pid(pid: int) -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM hotspots WHERE pid = ?", (pid,))
        rows = await cursor.fetchall()
        return rows

async def db_get_hotspot_by_id(id: int) -> Union[Hotspot, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM hotspots WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if row:
            return Hotspot(
                id=row["id"],
                number=row["number"],
                latlon=row["latlon"],
                pid=row["pid"],
            )
        return row

async def db_add_hotspot(hotspot: Hotspot) -> None:
    async with get_db() as db:
        await db.execute("""
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
        await db.execute("""
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

async def db_delete_hotspot(id: int) -> None:
    async with get_db() as db:
        await db.execute("DELETE FROM hotspots WHERE id = ?", (id,))
        await db.commit()

async def db_get_menus() -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM menus")
        rows = await cursor.fetchall()
        return rows

async def db_get_menus_by_rid(rid: int) -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM menus WHERE rid = ?", (rid,))
        rows = await cursor.fetchall()
        return rows

async def db_get_menu_by_id(id: int) -> Union[Menu, None]:
    async with get_db() as db:
        cursor = await db.execute("SELECT * FROM menus WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if row:
            return Menu(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                category=row["category"],
                photo=row["photo"],
                price=row["price"],
                rid=row["rid"],
            )
        return row

async def db_add_menu(menu: Menu) -> None:
    async with get_db() as db:
        await db.execute("""
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
        await db.execute("""
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

async def db_update_menu_photo(url: str, id: int) -> None:
    async with get_db() as db:
        await db.execute("UPDATE menus SET photo = ? WHERE id = ?", (url, id))
        await db.commit()

async def db_delete_menu(id: int) -> None:
    async with get_db() as db:
        await db.execute("DELETE FROM menus WHERE id = ?", (id,))
        await db.commit()
