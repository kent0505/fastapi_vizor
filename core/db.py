from contextlib  import asynccontextmanager
from dataclasses import dataclass
from typing      import AsyncGenerator

import aiosqlite

@asynccontextmanager
async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    db = await aiosqlite.connect("sqlite.db")
    db.row_factory = aiosqlite.Row  # To return dict-like rows
    try:
        yield db
    finally:
        await db.close()

_id:   str = "id INTEGER PRIMARY KEY"
_text: str = "TEXT NOT NULL"
_int:  str = "INTEGER NOT NULL"

@dataclass
class Tables:
    users:       str = "users"
    restaurants: str = "restaurants"
    photos:      str = "photos"
    hotspots:    str = "hotspots"
    reserves:    str = "reserves"

@dataclass
class Sql:
    users: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.users} (
            {_id},
            name  {_text},
            phone {_text},
            age   {_int},
            photo {_text} DEFAULT ''
        );
    """
    restaurants: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.restaurants} (
            {_id},
            title     {_text},
            type      {_text},
            photo     {_text},
            phone     {_text},
            instagram {_text},
            address   {_text},
            latlon    {_text},
            hours     {_text},
            position  {_int}
        );
    """
    photos: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.photos} (
            {_id},
            url {_text},
            rid {_int}
        );
    """
    hotspots: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.hotspots} (
            {_id},
            number {_int},
            latlon {_text},
            pid    {_int}
        );
    """
    reserves: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.reserves} (
            {_id},
            uid    {_int},
            rid    {_int},
            number {_int},
            time   {_int},
            date   {_int},
            status {_text},
            note   {_text}
        );
    """
