from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer, Roles
from core.schemas import Menu
from core.settings import settings
from core.utils import get_format
from core.s3 import delete_object, put_object
from core.db import (
    db_get_restaurant_by_id,
    db_get_menus_by_rid,
    db_get_menu_by_id,
    db_add_menu,
    db_update_menu,
    db_update_menu_photo,
    db_delete_menu,
)

router = APIRouter()

@router.get("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def get_hotspots(rid: int):
    rows = await db_get_menus_by_rid(rid)

    return {
        "rid": rid,
        "hotspots": rows,
    }

@router.post("/", dependencies=[Depends(JWTBearer())])
async def add_menu(body: Menu):
    row = await db_get_restaurant_by_id(body.rid)
    if not row:
        raise HTTPException(404, "restaurant not found")

    await db_add_menu(body)

    return {"message": "menu added"}

@router.put("/", dependencies=[Depends(JWTBearer())])
async def edit_menu(body: Menu):
    row = await db_get_menu_by_id(body.id)
    if not row:
        raise HTTPException(404, "menu not found")

    await db_update_menu(body)

    return {"message": "menu updated"}

@router.patch("/", dependencies=[Depends(JWTBearer())])
async def edit_menu_photo(id: int, file: UploadFile = File()):
    row = await db_get_menu_by_id(id)
    if not row:
        raise HTTPException(404, "menu not found")
    
    format = get_format(str(file.filename))
    if format not in settings.image_formats:
        raise HTTPException(400, 'file error')

    key = f"menus/{id}.{format}"

    await delete_object(f"menus/{id}.{get_format(row.photo)}")
    await put_object(key, file)

    await db_update_menu_photo(key, id)

    return {"message": "menu photo updated"}

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_menu(id: int):
    row = await db_get_menu_by_id(id)
    if not row:
        raise HTTPException(404, "menu not found")
    
    await delete_object(f"menus/{id}.{get_format(row.photo)}")
    
    await db_delete_menu(id)
    
    return {"message": "menu deleted"}
