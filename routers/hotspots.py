from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import SessionDep, BaseModel
from db.panorama import db_get_panorama_by_id
from db.hotspot import (
    Hotspot,
    db_get_hotspot_by_id,
    db_add_hotspot,
    db_delete_hotspot,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

class HotspotSchema(BaseModel):
    number: int
    latlon: str
    pid: int

@router.post("/")
async def add_hotspot(
    body: HotspotSchema,
    db: SessionDep,
):
    row = await db_get_panorama_by_id(db, body.pid)
    if not row:
        raise HTTPException(404, "panorama not found")

    hotspot = Hotspot(
        number=body.number,
        latlon=body.latlon,
        pid=body.pid
    )
    await db_add_hotspot(db, hotspot)

    return {"message": "hotspot added"}

@router.put("/")
async def edit_hotspot(
    id: int,
    body: HotspotSchema,
    db: SessionDep,
):
    hotspot = await db_get_hotspot_by_id(db, id)
    if not hotspot:
        raise HTTPException(404, "hotspot not found")

    panorama = await db_get_panorama_by_id(db, body.pid)
    if not panorama:
        raise HTTPException(404, "panorama not found")

    hotspot.number = body.number
    hotspot.latlon = body.latlon
    hotspot.pid = body.pid
    await db.commit()

    return {"message": "hotspot updated"}

@router.delete("/")
async def delete_hotspot(
    id: int,
    db: SessionDep,
):
    row = await db_get_hotspot_by_id(db, id)
    if not row:
        raise HTTPException(404, "hotspot not found")

    await db_delete_hotspot(db, id)

    return {"message": "hotspot deleted"}
