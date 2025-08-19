from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from db import SessionDep, BaseModel, select
from db.panorama import Panorama
from db.hotspot import Hotspot

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
    panorama = await db.scalar(select(Panorama).filter_by(id=body.pid))
    if not panorama:
        raise HTTPException(404, "panorama not found")

    hotspot = Hotspot(
        number=body.number,
        latlon=body.latlon,
        pid=body.pid
    )
    db.add(hotspot)
    await db.commit()

    return {"message": "hotspot added"}

@router.put("/")
async def edit_hotspot(
    id: int,
    body: HotspotSchema,
    db: SessionDep,
):
    hotspot = await db.scalar(select(Hotspot).filter_by(id=id))
    if not hotspot:
        raise HTTPException(404, "hotspot not found")

    panorama = await db.scalar(select(Panorama).filter_by(id=body.pid))
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
    hotspot = await db.scalar(select(Hotspot).filter_by(id=id))
    if not hotspot:
        raise HTTPException(404, "hotspot not found")

    await db.delete(hotspot)
    await db.commit()

    return {"message": "hotspot deleted"}
