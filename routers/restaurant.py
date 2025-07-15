from fastapi       import APIRouter, HTTPException, Depends
from pydantic      import BaseModel
from core.security import JWTBearer
from core.db       import Tables, get_db 
from core.settings import settings

router = APIRouter(dependencies=[Depends(JWTBearer())])

class RestaurantModel(BaseModel):
    title:     str
    type:      str
    photo:     str
    phone:     str
    instagram: str
    address:   str
    latlon:    str
    hours:     str
    position:  int

@router.get("/",dependencies=[])
async def get_restaurants():
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.restaurants}")
        rows = await cursor.fetchall()
        return {Tables.restaurants: [dict(row) for row in rows]}

@router.post("/")
async def add_restaurant(body: RestaurantModel):
    async with get_db() as db:
        await db.execute(f"""
            INSERT INTO {Tables.restaurants} (title, type, photo, phone, instagram, address, latlon, hours, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            body.title,
            body.type,
            body.photo,
            body.phone,
            body.instagram,
            body.address,
            body.latlon,
            body.hours,
            body.position,
        ))
        await db.commit()
        return {"message": "restaurant added"}

@router.put("/{id}")
async def edit_restaurant(id: int, body: RestaurantModel):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.restaurants} WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(404, "restaurant not found")

        await db.execute(f"""
        UPDATE {Tables.restaurants} SET 
            title = ?, 
            type = ?, 
            photo = ?, 
            phone = ?, 
            instagram = ?,
            address = ?, 
            latlon = ?, 
            hours = ?, 
            position = ? 
        WHERE id = ?""", (
            body.title,
            body.type,
            body.photo,
            body.phone,
            body.instagram,
            body.address,
            body.latlon,
            body.hours,
            body.position,
            id
        ))
        await db.commit()
        return {"message": "restaurant updated"}

@router.delete("/{id}")
async def delete_restaurant(id: int):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.restaurants} WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(404, "Restaurant not found")

        await db.execute(f"DELETE FROM {Tables.restaurants} WHERE id = ?", (id,))
        await db.commit()
        return {"message": "restaurant deleted"}
