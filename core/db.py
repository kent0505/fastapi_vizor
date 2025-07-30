from contextlib import asynccontextmanager
from typing import AsyncGenerator, Union, List, Type, TypeVar
from pydantic import BaseModel
from enum import Enum
from core.schemas import (
    User, 
    Restaurant,
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

class Tables(str, Enum):
    users = "users"
    restaurants = "restaurants"
    panoramas = "panoramas"
    hotspots = "hotspots"
    menus = "menus"
    reserves = "reserves"

class Wheres(str, Enum):
    id = "id"
    phone = "phone"

def row_to_model(
    model_class: Type[BaseModel], 
    row: Union[aiosqlite.Row, None],
) -> Union[BaseModel, None]:
    if row is None: 
        return None
    return model_class(**dict(row))

T = TypeVar("T", bound=BaseModel)

# GET BY
async def db_get_by_id(
    model: Type[T], 
    table: Tables,
    id: int,
    where: Wheres = Wheres.id,
) -> Union[T, None]:
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {table.value} WHERE {where.value} = ?", (id,))
        row = await cursor.fetchone()
        return row_to_model(model, row)

# GET LIST
async def db_get_list(table: Tables) -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {table.value}")
        rows = await cursor.fetchall()
        return rows

# GET LIST BY
async def db_get_list_by(
    table: Tables, 
    where: str, 
    value: int
) -> List[aiosqlite.Row]:
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {table.value} WHERE {where} = ?", (value,))
        rows = await cursor.fetchall()
        return rows

# DELETE
async def db_delete(
    table: Tables, 
    id: int,
) -> List[aiosqlite.Row]:
    async with get_db() as db:
        await db.execute(f"DELETE FROM {table.value} WHERE id = ?", (id,))
        await db.commit()

# UPDATE PHOTO
async def db_update_photo(
    table: Tables, 
    url: str, 
    id: int,
) -> None:
    async with get_db() as db:
        await db.execute(f"UPDATE {table.value} SET photo = ? WHERE id = ?", (url, id))
        await db.commit()

# USER
async def db_add_user(user: User, role: str) -> None:
    async with get_db() as db:
        await db.execute("""
            INSERT INTO users (
                name,
                phone,
                password,
                age,
                role
            ) VALUES (?, ?, ?, ?, ?)""", (
            user.name, 
            user.phone, 
            user.password,
            user.age,
            role,
        ))
        await db.commit()

async def db_update_user(user: User) -> None:
    async with get_db() as db:
        await db.execute("""
            UPDATE users SET 
                name = ?, 
                phone = ?, 
                password = ?,
                age = ? 
            WHERE id = ?""", (
            user.name,
            user.phone,
            user.password,
            user.age,
            user.id,
        ))
        await db.commit()

# RESTAURANT
async def db_add_restaurant(restaurant: Restaurant) -> None:
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO {Tables.restaurants} (
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
            UPDATE {Tables.restaurants} SET 
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

# PANORAMA
async def db_add_panorama(photo: str, rid: int) -> None:
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO {Tables.panoramas} (
                photo, 
                rid
            ) VALUES (?, ?)""", (
            photo, 
            rid,
        ))
        await db.commit()

# HOTSPOT
async def db_add_hotspot(hotspot: Hotspot) -> None:
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO {Tables.hotspots} (
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
        await db.execute(f"""
            UPDATE {Tables.hotspots} SET 
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

# MENU
async def db_add_menu(menu: Menu) -> None:
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO {Tables.menus} (
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
            UPDATE {Tables.menus} SET 
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
