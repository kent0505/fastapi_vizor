from fastapi       import APIRouter, HTTPException, Depends
from pydantic      import BaseModel
from core.security import JWTBearer, Roles
from core.db       import Tables, get_db 

router = APIRouter()

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

@router.get("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def get_restaurants():
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.restaurants}")
        rows = await cursor.fetchall()

        return {"restaurants": [dict(row) for row in rows]}

@router.post("/", dependencies=[Depends(JWTBearer())])
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
            body.position
        ))
        await db.commit()

        return {"message": "restaurant added"}

@router.put("/", dependencies=[Depends(JWTBearer())])
async def edit_restaurant(id: int, body: RestaurantModel):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.restaurants} WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="restaurant not found")

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

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_restaurant(id: int):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.restaurants} WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="restaurant not found")

        await db.execute(f"DELETE FROM {Tables.restaurants} WHERE id = ?", (id,))
        await db.commit()

        return {"message": "restaurant deleted"}
