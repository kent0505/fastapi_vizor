from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import SessionDep, BaseModel, select
from db.restaurant import Restaurant
from db.panorama import Panorama
from db.hotspot import Hotspot
from db.table import RestaurantTable

router = APIRouter(dependencies=[Depends(JWTBearer())])

class HotspotSchema(BaseModel):
    lat: str
    lon: str
    rid: int
    pid: int
    tid: int

class CoordinatesSchema(BaseModel):
    lat: str
    lon: str

@router.post("/")
async def add_hotspot(
    body: HotspotSchema,
    db: SessionDep,
):
    restaurant = await db.scalar(select(Restaurant).filter_by(id=body.pid))
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    panorama = await db.scalar(select(Panorama).filter_by(id=body.pid))
    if not panorama:
        raise HTTPException(404, "panorama not found")

    table = await db.scalar(select(RestaurantTable).filter_by(id=body.tid))
    if not table:
        raise HTTPException(404, "table not found")

    if panorama.rid != table.rid:
        raise HTTPException(400, "panorama and table belong to different restaurants")

    hotspot = Hotspot(
        lat=body.lat,
        lon=body.lon,
        rid=body.rid,
        pid=body.pid,
        tid=body.tid,
    )
    db.add(hotspot)
    await db.commit()

    return {"message": "hotspot added"}

@router.put("/")
async def edit_hotspot_coordinates(
    id: int,
    body: CoordinatesSchema,
    db: SessionDep,
):
    hotspot = await db.scalar(select(Hotspot).filter_by(id=id))
    if not hotspot:
        raise HTTPException(404, "hotspot not found")

    hotspot.lat = body.lat
    hotspot.lon = body.lon
    await db.commit()

    return {"message": "hotspot updated"}

@router.delete("/")
async def delete_hotspot(
    id: int,
    db: SessionDep,
):
    hotspot = await db.scalar(select(Hotspot).filter_by(id=id))
    if not hotspot:
        raise HTTPException(404, "hotspot not found")

    await db.delete(hotspot)
    await db.commit()

    return {"message": "hotspot deleted"}
