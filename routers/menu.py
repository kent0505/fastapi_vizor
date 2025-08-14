from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.s3 import put_object, delete_object
from db import SessionDep, BaseModel
from db.restaurant import db_get_restaurant_by_id
from db.category import db_get_category_by_id
from db.menu import Menu, db_get_menu_by_id

router = APIRouter(dependencies=[Depends(JWTBearer())])

class Menu(BaseModel):
    title: str
    description: str
    price: str
    currency: str
    cid: int
    rid: int

@router.post("/")
async def add_menu(
    body: Menu,
    db: SessionDep,
):
    restaurant = await db_get_restaurant_by_id(body.rid)
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    category = await db_get_category_by_id(body.cid)
    if not category:
        raise HTTPException(404, "category not found")

    menu = Menu(
        title=body.title,
        description=body.description,
        price=body.price,
        currency=body.currency,
        cid=body.cid,
        rid=body.rid,
    )
    db.add(menu)
    await db.commit()

    return {"message": "menu added"}

@router.put("/")
async def edit_menu(
    id: int,
    body: Menu,
    db: SessionDep,
):
    menu = await db_get_menu_by_id(db, id)
    if not menu:
        raise HTTPException(404, "menu not found")

    restaurant = await db_get_restaurant_by_id(body.rid)
    if not restaurant:
        raise HTTPException(404, "restaurant not found")

    category = await db_get_category_by_id(body.cid)
    if not category:
        raise HTTPException(404, "category not found")

    menu.title=body.title,
    menu.description=body.description,
    menu.price=body.price,
    menu.currency=body.currency,
    menu.cid=body.cid,
    menu.rid=body.rid,
    await db.commit()

    return {"message": "menu updated"}

@router.patch("/")
async def edit_menu_photo(
    id: int, 
    db: SessionDep,
    file: UploadFile = File(),
):
    menu = await db_get_menu_by_id(db, id)
    if not menu:
        raise HTTPException(404, "menu not found")

    key = f"menus/{id}"

    photo =  await put_object(key, file)

    menu.photo = photo
    await db.commit()

    return {"message": "menu photo updated"}

@router.delete("/")
async def delete_menu(
    id: int,
    db: SessionDep,
):
    menu = await db_get_menu_by_id(db, id)
    if not menu:
        raise HTTPException(404, "menu not found")

    key = f"menus/{menu.id}"
    await delete_object(key)

    await db.delete(menu)
    await db.commit()

    return {"message": "menu deleted"}
