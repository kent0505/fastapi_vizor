from fastapi           import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic          import BaseModel
from core.security     import JWTBearer, signJWT
from core.db           import Tables, get_db
from core.settings     import settings
from core.utils        import get_timestamp

router = APIRouter()

class LoginModel(BaseModel):
    phone:    str
    password: str

class RegisterModel(BaseModel):
    name:  str
    phone: str
    age:   int

@router.post("/login")
async def login(body: LoginModel):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.users} WHERE phone = ?", (body.phone,))
        row = await cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="phone number does not exist")
        
        now = get_timestamp()
        id = row["id"]
        role = settings.user
        exp = now + settings.year_seconds
        if body.password == settings.password:
            role = settings.admin
            exp = now + settings.day_seconds

        access_token: str = signJWT(id, role, exp)

        return {
            "access_token": access_token,
            "role": role,
        }

@router.post("/register")
async def register(body: RegisterModel):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT id FROM {Tables.users} WHERE phone = ?", (body.phone,))
        exists = await cursor.fetchone()
        if exists:
            raise HTTPException(status_code=400, detail="user already exists")

        await db.execute(
            f"INSERT INTO {Tables.users} (name, phone, age) VALUES (?, ?, ?)", 
            (body.name, body.phone, body.age)
        )
        await db.commit()
        return {"message": "user registered"}

@router.delete("/{id}", dependencies=[Depends(JWTBearer(role=settings.admin))], include_in_schema=False)
async def delete_user_from_home(id: int):
    async with get_db() as db:
        await db.execute(f"DELETE FROM {Tables.users} WHERE id = ?", (id,))
        await db.commit()
    return RedirectResponse(url="/", status_code=303)
