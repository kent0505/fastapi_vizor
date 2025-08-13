from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from core.security import Roles
from db import BaseModel, SessionDep
from db.user import (
    User,
    db_get_users,
    db_get_user_by_id,
    db_get_user_by_phone,
    db_add_user,
    db_delete_user,
)

router = APIRouter(dependencies=[Depends(JWTBearer())])

class UserSchema(BaseModel):
    phone: str
    name: str
    age: str
    fcm: str

@router.get("/")
async def get_users(db: SessionDep):
    rows = await db_get_users(db)

    return {"users": rows}

@router.post("/")
async def add_admin(
    body: UserSchema, 
    role: Roles,
    db: SessionDep,
):
    row = await db_get_user_by_phone(db, body.phone)
    if row:
        raise HTTPException(409, "user already exists")

    user = User(
        phone=body.phone,
        name=body.name,
        age=body.age,
        role=role.value,
    )
    await db_add_user(db, user)

    return {"message": f"{role.value} registered"}

@router.put("/")
async def edit_admin(
    id: int,
    body: UserSchema,
    role: Roles,
    db: SessionDep,
):
    row = await db_get_user_by_id(db, id)
    if not row:
        raise HTTPException(404, "user not found")

    row.name=body.name
    row.age=body.age
    row.fcm=body.fcm
    row.role=role.value
    await db.commit()

    return {"message": "user updated"}

@router.delete("/")
async def delete_admin(
    id: int,
    db: SessionDep,
):
    row = await db_get_user_by_id(db, id)
    if not row:
        raise HTTPException(404, "user not found")

    await db_delete_user(db, row)

    return {"message": "user deleted"}
