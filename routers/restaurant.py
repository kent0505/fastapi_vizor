from fastapi import APIRouter, Depends
from core.security import JWTBearer, Roles

router = APIRouter(dependencies=[Depends(JWTBearer())])

# @router.post("/")
# async def add_restaurant(body: Restaurant):
#     await db_add_restaurant(body)

#     return {"message": "restaurant added"}

# @router.put("/")
# async def edit_restaurant(body: Restaurant):
#     row = await db_get_restaurant_by_id(body.id)
#     if not row:
#         raise HTTPException(404, "restaurant not found")

#     await db_update_restaurant(body)

#     return {"message": "restaurant updated"}

# @router.patch("/")
# async def edit_restaurant_photo(id: int, file: UploadFile = File()):
#     row = await db_get_restaurant_by_id(id)
#     if not row:
#         raise HTTPException(404, "restaurant not found")
    
#     format = get_format(str(file.filename))
#     if format not in settings.image_formats:
#         raise HTTPException(400, 'file error')

#     key = f"restaurants/{id}.{format}"

#     await delete_object(f"restaurants/{id}.{get_format(row.photo)}")
#     await put_object(key, file)

#     await db_update_photo(Tables.restaurants, key, id)
    

#     return {"message": "restaurant photo updated"}

# @router.delete("/")
# async def delete_restaurant(id: int):
#     row = await db_get_by_id(Restaurant, Tables.restaurants, id)
#     if not row:
#         raise HTTPException(404, "restaurant not found")
    
#     await delete_object(f"restaurants/{id}.{get_format(row.photo)}")
    
#     await db_delete(Tables.restaurants, id)
    
#     return {"message": "restaurant deleted"}
