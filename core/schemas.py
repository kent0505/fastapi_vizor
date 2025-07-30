from pydantic import BaseModel
from typing import Optional
from dataclasses import dataclass

class LoginBody(BaseModel):
    phone: int
    password: str = ''

class User(BaseModel):
    id: Optional[int] = None
    name: str
    phone: str
    password: str
    age: int
    role: Optional[str] = None
    photo: Optional[str] = None

class Restaurant(BaseModel):
    id: Optional[int] = None
    title: str
    type: str
    photo: Optional[str] = None
    phone: str
    instagram: str
    address: str
    latlon: str
    hours: str
    position: int

class Panorama(BaseModel):
    id: Optional[int] = None
    photo: str
    rid: int

class Hotspot(BaseModel):
    id: Optional[int] = None
    number: int
    latlon: str
    pid: int

class Menu(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    category: str
    photo: Optional[str] = None
    price: str
    rid: int

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
            password {TEXT},
            age {INTEGER},
            role {TEXT},
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
    menus: str = f"""
        CREATE TABLE IF NOT EXISTS menus (
            {ID},
            title {TEXT},
            description {TEXT},
            category {TEXT},
            photo {TEXT} DEFAULT '',
            price {TEXT},
            rid {INTEGER}
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
