from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer, signJWT
from core.security import Roles
from core.settings import settings
from core.utils import (
    get_timestamp, 
    hash_password, 
    check_password,
)
from db.user import (
    User,
    LoginBody,
    db_get_user_by_id,
    db_get_user_by_phone,
    db_add_user,
    db_update_user,
    db_delete_user,
)

import random
import logging

router = APIRouter()

@router.post("/register")
async def register(phone: str):
    row = await db_get_user_by_phone(phone)
    if row:
        raise HTTPException(404, "user already exists")

    code = random.randint(10000, 99999)
    logging.info(code)

    await db_add_user(
        role=Roles.user,
        user=User(
            name="",
            phone=phone,
            password="",
            age=0,
            code=code,
        )
    )

    # send sms code

    return {"message": "sms code sent"}

@router.post("/login")
async def login(body: LoginBody):
    row = await db_get_user_by_phone(body.phone)
    if not row:
        raise HTTPException(404, "phone number does not exist")

    if row.code != body.code:
        raise HTTPException(400, "verification code is incorrect")
    
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

@router.post("/register/admin", dependencies=[Depends(JWTBearer())])
async def register(
    body: User, 
    role: Roles,
):
    row = await db_get_user_by_phone(body.phone)
    if row:
        raise HTTPException(404, "user already exists")

    body.password = hash_password(body.password)

    await db_add_user(body, role.value)

    return {"message": f"{role.value} registered"}

@router.put("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def edit_user(body: User):
    row = await db_get_user_by_id(body.id)
    if not row:
        raise HTTPException(404, "user does not exist")

    await db_update_user(body)

    return {"message": "user updated"}

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_user(id: int):
    row = await db_get_user_by_id(id)
    if not row:
        raise HTTPException(404, "user not found")

    await db_delete_user(id)

    return {"message": "user deleted"}
