from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer, Roles
from core.schemas import Hotspot
from core.db import (
    db_get_panorama_by_id,
    db_get_hotspots_by_pid,
    db_get_hotspot_by_id,
    db_add_hotspot,
    db_update_hotspot,
    db_delete_hotspot,
)

router = APIRouter()

@router.get("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def get_hotspots(pid: int):
    rows = await db_get_hotspots_by_pid(pid)

    return {
        "pid": pid,
        "hotspots": rows,
    }

@router.post("/", dependencies=[Depends(JWTBearer())])
async def add_hotspot(body: Hotspot):
    row = await db_get_panorama_by_id(body.pid)
    if not row:
        raise HTTPException(404, "panorama not found")

    await db_add_hotspot(body)

    return {"message": "hotspot added"}

@router.put("/", dependencies=[Depends(JWTBearer())])
async def edit_hotspot(body: Hotspot):
    row = await db_get_hotspot_by_id(body.id)
    if not row:
        raise HTTPException(404, "hotspot not found")
    
    row = await db_get_panorama_by_id(body.pid)
    if not row:
        raise HTTPException(404, "panorama not found")
    
    await db_update_hotspot(body)

    return {"message": "hotspot updated"}

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_hotspot(id: int):
    row = await db_get_hotspot_by_id(id)
    if not row:
        raise HTTPException(404, "hotspot not found")
    
    await db_delete_hotspot(id)
    
    return {"message": "hotspot deleted"}
