from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer, Roles
from db.city import db_get_cities, db_get_city_by_id
from db.restaurant import db_get_restaurants_by_city

router = APIRouter(
    dependencies=[
        Depends(JWTBearer(role=Roles.user)),
    ]
)

@router.get("/cities")
async def get_cities():
    rows = await db_get_cities()

    return {"cities": rows}

@router.get("/restaurants")
async def get_restaurants(city: int):
    row = await db_get_city_by_id(city)
    if not row:
        raise HTTPException(404, "city not found")

    rows = await db_get_restaurants_by_city(city)

    return {
        "city": row.name,
        "restaurants": rows,
    }

# @router.get("/panoramas")
# async def get_panoramas(rid: int):
#     rows = await db_get_list_by(Tables.panoramas, "rid", rid)

#     return {
#         "rid": rid,
#         "panoramas": rows,
#     }

# @router.get("/hotspots")
# async def get_hotspots(pid: int):
#     rows = await db_get_list_by(Tables.hotspots, "pid", pid)

#     return {
#         "pid": pid,
#         "hotspots": rows,
#     }

# @router.get("/menus")
# async def get_menus(rid: int):
#     rows = await db_get_list_by(Tables.menus, "rid", rid)

#     return {
#         "rid": rid,
#         "menus": rows,
#     }
