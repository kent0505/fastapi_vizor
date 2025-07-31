from fastapi import APIRouter, Depends
from core.security import JWTBearer, Roles

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.user))])

# @router.get("/restaurants")
# async def get_restaurants():
#     rows = await db_get_list(Tables.restaurants)

#     return {"restaurants": rows}

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
