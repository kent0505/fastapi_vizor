from fastapi import APIRouter
from db import BaseModel, SessionDep

router = APIRouter()

class Hotspot(BaseModel):
    number: int
    latlon: str
    pid: int

# @router.post("/")
# async def add_hotspot(body: Hotspot):
#     row = await db_get_by_id(Panorama, Tables.panoramas, body.pid)
#     if not row:
#         raise HTTPException(404, "panorama not found")

#     await db_add_hotspot(body)

#     return {"message": "hotspot added"}

# @router.put("/")
# async def edit_hotspot(body: Hotspot):
#     row = await db_get_by_id(Hotspot, Tables.hotspots, body.id)
#     if not row:
#         raise HTTPException(404, "hotspot not found")
    
#     row = await db_get_by_id(body.pid)
#     if not row:
#         raise HTTPException(404, "panorama not found")
    
#     await db_update_hotspot(body)

#     return {"message": "hotspot updated"}

# @router.delete("/")
# async def delete_hotspot(id: int):
#     row = await db_get_by_id(Hotspot, Tables.hotspots, id)
#     if not row:
#         raise HTTPException(404, "hotspot not found")
    
#     await db_delete(Tables.hotspots, id)
    
#     return {"message": "hotspot deleted"}
