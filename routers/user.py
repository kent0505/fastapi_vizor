from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer
from core.security import Roles
from core.s3 import put_object
from db.user import (
    User,
    db_get_user_by_id,
    db_update_user,
)

router = APIRouter(dependencies=[Depends(JWTBearer(role=Roles.user))])

@router.put("/")
async def edit_user(body: User):
    row = await db_get_user_by_id(body.id)
    if not row:
        raise HTTPException(404, "user not found")
    
    if row.phone != body.phone:
        raise HTTPException(404, "phone number not found")

    await db_update_user(
        role=row.role, 
        user=body,
    )

    return {"message": "user updated"}

@router.post("/")
async def add_user_photo(
    id: int, 
    file: UploadFile = File(),
):
    row = await db_get_user_by_id(id)
    if not row:
        raise HTTPException(404, "user not found")
    
    key = f"users/{id}"

    photo = await put_object(key, file)

    return {
        "message": "user photo added",
        "photo": photo,
    }
