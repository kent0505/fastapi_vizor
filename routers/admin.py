from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from core.security import Roles
from db.user import (
    User,
    db_get_users,
    db_get_user_by_id,
    db_get_user_by_phone,
    db_add_user,
    db_update_user,
    db_delete_user,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

@router.get("/")
async def get_users():
    rows = await db_get_users()

    return {"users": rows}

@router.post("/")
async def add_admin(
    body: User, 
    role: Roles,
):
    row = await db_get_user_by_phone(body.phone)
    if row:
        raise HTTPException(409, "user already exists")

    await db_add_user(body, role.value)

    return {"message": f"{role.value} registered"}

@router.put("/")
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

@router.delete("/")
async def delete_admin(id: int):
    row = await db_get_user_by_id(id)
    if not row:
        raise HTTPException(404, "user not found")

    await db_delete_user(id)

    return {"message": "user deleted"}
