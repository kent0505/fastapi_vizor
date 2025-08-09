from fastapi import APIRouter, HTTPException
from core.security import Roles, signJWT
from core.settings import settings
from core.sms import send_sms
from core.utils import (
    get_timestamp, 
    generate_code,
)
from db.user import (
    User,
    LoginBody,
    db_get_user_by_phone,
    db_add_user,
    db_update_user,
)

router = APIRouter()

@router.post("/send_code")
async def send_code(phone: str):
    code = generate_code()

    await send_sms(
        str(code),
        phone,
    )

    row = await db_get_user_by_phone(phone)

    if row:
        row.code = code
        await db_update_user(
            role=row.role,
            user=row,
        )
    else:
        await db_add_user(
            role=Roles.user,
            user=User(
                phone=phone,
                code=code,
            )
        )

    return {"message": "sms code sent"}

@router.post("/login")
async def login(body: LoginBody):
    row = await db_get_user_by_phone(body.phone)
    if not row:
        raise HTTPException(404, "phone number does not exist")

    if row.code is None:
        raise HTTPException(400, "verification code not sent")

    if row.code != body.code:
        raise HTTPException(400, "verification code is incorrect")

    row.code = None
    await db_update_user(
        role=row.role,
        user=row,
    )

    access_token: str = signJWT(
        row.id, 
        row.role, 
        get_timestamp() + settings.year_seconds,
    )

    return {
        "access_token": access_token,
        "role": row.role,
    }
