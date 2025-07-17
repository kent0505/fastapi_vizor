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

ID      = "id INTEGER PRIMARY KEY"
TEXT    = "TEXT NOT NULL"
INTEGER = "INTEGER NOT NULL"

@dataclass
class Tables:
    users:       str = "users"
    restaurants: str = "restaurants"
    panoramas:   str = "panoramas"
    hotspots:    str = "hotspots"
    reserves:    str = "reserves"

@dataclass
class Sql:
    users: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.users} (
            {ID},
            name  {TEXT},
            phone {TEXT},
            age   {INTEGER},
            photo {TEXT} DEFAULT ''
        );
    """
    restaurants: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.restaurants} (
            {ID},
            title     {TEXT},
            type      {TEXT},
            photo     {TEXT} DEFAULT '',
            phone     {TEXT},
            instagram {TEXT},
            address   {TEXT},
            latlon    {TEXT},
            hours     {TEXT},
            position  {INTEGER}
        );
    """
    panoramas: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.panoramas} (
            {ID},
            url {TEXT},
            rid {INTEGER}
        );
    """
    hotspots: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.hotspots} (
            {ID},
            number {INTEGER},
            latlon {TEXT},
            pid    {INTEGER}
        );
    """
    reserves: str = f"""
        CREATE TABLE IF NOT EXISTS {Tables.reserves} (
            {ID},
            uid    {INTEGER},
            rid    {INTEGER},
            number {INTEGER},
            time   {INTEGER},
            date   {INTEGER},
            status {TEXT},
            note   {TEXT}
        );
    """
