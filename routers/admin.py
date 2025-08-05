from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from core.security import Roles
from db.user import (
    User,
    db_get_user_by_id,
    db_get_user_by_phone,
    db_add_user,
    db_update_user,
    db_delete_user,
)

router = APIRouter()

@router.post("/admin", dependencies=[Depends(JWTBearer())])
async def add_admin(
    body: User, 
    role: Roles,
):
    row = await db_get_user_by_phone(body.phone)
    if row:
        raise HTTPException(409, "user already exists")

    await db_add_user(body, role.value)

    return {"message": f"{role.value} registered"}

@router.put("/admin", dependencies=[Depends(JWTBearer())])
async def edit_admin(
    body: User,
    role: Roles,
):
    row = await db_get_user_by_id(body.id)
    if not row:
        raise HTTPException(404, "user not found")

    await db_update_user(
        role=role, 
        user=body,
    )

    return {"message": "user updated"}

@router.delete("/admin", dependencies=[Depends(JWTBearer())])
async def delete_admin(id: int):
    row = await db_get_user_by_id(id)
    if not row:
        raise HTTPException(404, "user not found")

    await db_delete_user(id)

    return {"message": "user deleted"}
