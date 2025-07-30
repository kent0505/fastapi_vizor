from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer, Roles, signJWT
from core.schemas import User, LoginBody
from core.settings import settings
from core.utils import check_password, hash_password
from core.utils import get_timestamp, get_format
from core.s3 import delete_object
from core.db import (
    Tables,
    Wheres,
    db_get_by_id, 
    db_get_list,
    db_add_user,
    db_delete,
)

router = APIRouter()

@router.post("/login")
async def login(body: LoginBody):
    row = await db_get_by_id(
        User, 
        Tables.users, 
        body.phone, 
        Wheres.phone,
    )
    if not row:
        raise HTTPException(404, "phone number does not exist")

    hashed = check_password(body.password, row.password)

    if not hashed:
        raise HTTPException(401, "invalid password")

    access_token: str = signJWT(
        row.id, 
        row.role, 
        get_timestamp() + settings.year_seconds,
    )

    return {
        "access_token": access_token,
        "role": row.role,
    }

@router.post("/register")
async def register(body: User):
    row = await db_get_by_id(
        User, 
        Tables.users, 
        body.phone, 
        Wheres.phone
    )
    if row:
        raise HTTPException(404, "user already exists")

    rows = await db_get_list(Tables.users)

    body.password = hash_password(body.password)
    
    await db_add_user(
        body, 
        Roles.admin if not rows else Roles.user
    )

    return {"message": "user registered"}

@router.post("/register/admin", dependencies=[Depends(JWTBearer())])
async def register(
    body: User, 
    role: Roles,
):
    row = await db_get_by_id(
        User, 
        Tables.users, 
        body.phone, 
        Wheres.phone
    )
    if row:
        raise HTTPException(404, "user already exists")
    
    body.password = hash_password(body.password)

    await db_add_user(body, role.value)

    return {"message": f"{role.value} registered"}

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_user(id: int):
    row = await db_get_by_id(User, Tables.users, id)
    if not row:
        raise HTTPException(404, "user not found")
    
    await delete_object(f"users/{id}.{get_format(row.photo)}") 

    await db_delete(Tables.users, id)

    return {"message": "user deleted"}
