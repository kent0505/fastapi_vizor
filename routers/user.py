from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer, signJWT
from core.security import Roles
from core.settings import settings
from core.utils import (
    get_timestamp, 
    generate_code,
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
)

router = APIRouter()

@router.post("/send_code")
async def send_code(phone: str):
    code = generate_code()

    # send sms code

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

    if row.code is None or row.code != body.code:
        raise HTTPException(400, "verification code is incorrect")
    
    hashed = check_password(body.password, row.password)

    if row.password and not hashed:
        raise HTTPException(401, "invalid password")

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

@router.put("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
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
