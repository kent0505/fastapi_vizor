from fastapi import APIRouter, HTTPException, Depends
from core.security import JWTBearer
from core.security import Roles, UserDep
from db import SessionDep, BaseModel, select
from db.user import User

router = APIRouter(dependencies=[Depends(JWTBearer())])

class UserSchema(BaseModel):
    phone: str
    name: str
    age: str

@router.get("/")
async def get_users(db: SessionDep):
    users = (await db.scalars(select(User))).all()

    return {"users": users}

@router.post("/")
async def add_admin(
    body: UserSchema, 
    role: Roles,
    db: SessionDep,
):
    user = await db.scalar(select(User).filter_by(phone=body.phone))
    if user:
        raise HTTPException(409, "user already exists")

    user = User(
        phone=body.phone,
        name=body.name,
        age=body.age,
        role=role.value,
    )
    db.add(user)
    await db.commit()

    return {"message": f"{role.value} added"}

@router.put("/")
async def edit_admin(
    body: UserSchema,
    role: Roles,
    db: SessionDep,
):
    user = await db.scalar(select(User).filter_by(phone=body.phone))
    if not user:
        raise HTTPException(404, "user not found")
    
    if user.phone == body.phone:
        raise HTTPException(409, "phone already exists")

    user.phone=body.phone
    user.name=body.name
    user.age=body.age
    user.role=role.value
    await db.commit()

    return {"message": "user updated"}

@router.delete("/")
async def delete_admin(
    id: int,
    admin: UserDep,
    db: SessionDep,
):
    user = await db.scalar(select(User).filter_by(id=id))
    if not user:
        raise HTTPException(404, "user not found")
    
    if id == admin:
        raise HTTPException(403, "admin can't delete itself")

    await db.delete(user)
    await db.commit()

    return {"message": "user deleted"}
