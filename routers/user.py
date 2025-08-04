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

@router.post("/register")
async def register(phone: str):
    code = generate_code()

    # send sms code

    row = await db_get_user_by_phone(phone)

    if row:
        await db_update_user(
            role=row.role,
            user=User(
                id=row.id,
                name=row.name,
                phone=row.phone,
                password=row.password,
                age=row.age,
                code=code,
            )
        )
    else:
        await db_add_user(
            role=Roles.user,
            user=User(
                name="",
                phone=phone,
                password=hash_password(""),
                age=0,
                code=code,
            )
        )

    return {"message": "sms code sent"}

@router.post("/resend_code")
async def resend_code(phone: str):
    row = await db_get_user_by_phone(phone)
    if not row:
        raise HTTPException(404, "phone number does not exist")

    code = generate_code()

    # send sms code

    await db_update_user(
        role=row.role,
        user=User(
            id=row.id,
            name=row.name,
            phone=row.phone,
            password=row.password,
            age=row.age,
            code=code,
        )
    )

    return {"message": "sms code resent"}

@router.post("/login")
async def login(body: LoginBody):
    row = await db_get_user_by_phone(body.phone)
    if not row:
        raise HTTPException(404, "phone number does not exist")

    if row.code != body.code or row.code == 0:
        raise HTTPException(400, "verification code is incorrect")
    
    hashed = check_password(body.password, row.password)

    if not hashed:
        raise HTTPException(401, "invalid password")

    await db_update_user(
        role=row.role,
        user=User(
            id=row.id,
            name=row.name,
            phone=row.phone,
            password=row.password,
            age=row.age,
            code=0,
        )
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

    body.password = hash_password(body.password)
    await db_update_user(
        role=row.role, 
        user=body,
    )

    return {"message": "user updated"}
