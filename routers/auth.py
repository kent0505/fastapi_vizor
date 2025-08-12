from fastapi import APIRouter, HTTPException, Body, Depends
from core.security import Roles, signJWT
from core.config import settings
from core.sms import send_sms
from core.utils import get_timestamp, generate_code
from db import AsyncSession, db_helper
from db.user import (
    User,
    LoginBody,
    db_get_user_by_phone,
    db_add_user,
)

router = APIRouter()

@router.post("/send_code")
async def send_code(
    phone: str = Body,
    db: AsyncSession = Depends(db_helper.get_db),
):
    code = str(generate_code())

    await send_sms(code, phone)

    row = await db_get_user_by_phone(db, phone)

    if row:
        row.code = code
        await db.commit()
    else:
        await db_add_user(
            db,
            user=User(
                phone=phone,
                code=code,
                role=Roles.user,
            )
        )

    return {"message": "sms code sent"}

@router.post("/login")
async def login(
    body: LoginBody,
    db: AsyncSession = Depends(db_helper.get_db),
):
    row = await db_get_user_by_phone(db, body.phone)
    if not row:
        raise HTTPException(404, "phone number does not exist")

    if row.code is None:
        raise HTTPException(400, "verification code not sent")

    if row.code != body.code:
        raise HTTPException(400, "verification code is incorrect")

    row.code = None
    await db.commit()

    access_token: str = signJWT(
        row.id, 
        row.role, 
        get_timestamp() + settings.year_seconds,
    )

    return {
        "access_token": access_token,
        "role": row.role,
    }
