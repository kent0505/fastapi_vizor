from fastapi import APIRouter

router = APIRouter()

# @router.post("/")
# async def add_menu(body: Menu):
#     row = await db_get_by_id(Restaurant, Tables.restaurants, body.rid)
#     if not row:
#         raise HTTPException(404, "restaurant not found")

#     await db_add_menu(body)

#     return {"message": "menu added"}

# @router.put("/")
# async def edit_menu(body: Menu):
#     row = await db_get_by_id(Menu, Tables.menus, body.id)
#     if not row:
#         raise HTTPException(404, "menu not found")

#     await db_update_menu(body)

#     return {"message": "menu updated"}

# @router.patch("/")
# async def edit_menu_photo(id: int, file: UploadFile = File()):
#     row = await db_get_by_id(Menu, Tables.menus, id)
#     if not row:
#         raise HTTPException(404, "menu not found")
    
#     format = get_format(str(file.filename))
#     if format not in settings.image_formats:
#         raise HTTPException(400, 'file error')

#     key = f"menus/{id}.{format}"

#     await delete_object(f"menus/{id}.{get_format(row.photo)}")
#     await put_object(key, file)

#     await db_update_photo(Tables.menus, key, id)

#     return {"message": "menu photo updated"}

# @router.delete("/")
# async def delete_menu(id: int):
#     row = await db_get_by_id(Menu, Tables.menus, id)
#     if not row:
#         raise HTTPException(404, "menu not found")
    
#     await delete_object(f"menus/{id}.{get_format(row.photo)}")
    
#     await db_delete(Tables.menus, id)
    
#     return {"message": "menu deleted"}
