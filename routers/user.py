from fastapi       import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic      import BaseModel
from core.security import JWTBearer, Roles, signJWT
from core.db       import Tables, get_db
from core.utils    import get_timestamp
from core.settings import settings, s3

router = APIRouter()

class LoginModel(BaseModel):
    phone:    str
    password: str

class UserModel(BaseModel):
    name:  str
    phone: str
    age:   int

@router.post("/login")
async def login(body: LoginModel):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.users} WHERE phone = ?", (body.phone,))
        row = await cursor.fetchone()

        if not row:
            raise HTTPException(404, "phone number does not exist")
        
        now = get_timestamp()
        role = Roles.user
        exp = now + settings.year_seconds
        if body.password == settings.password:
            role = Roles.admin
            exp = now + settings.day_seconds

        access_token: str = signJWT(row["id"], role, exp)

        return {
            "access_token": access_token,
            "role": role,
        }

@router.post("/register")
async def register(body: UserModel):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT id FROM {Tables.users} WHERE phone = ?", (body.phone,))
        row = await cursor.fetchone()
        if row:
            raise HTTPException(400, "user already exists")

        await db.execute(
            f"INSERT INTO {Tables.users} (name, phone, age) VALUES (?, ?, ?)", 
            (body.name, body.phone, body.age)
        )
        await db.commit()
        return {"message": "user registered"}

@router.put("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def edit_user(id: int, body: UserModel):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.users} WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(404, "user not found")

        if row["phone"] != body.phone:
            cursor = await db.execute(f"SELECT * FROM {Tables.users} WHERE phone = ?", (body.phone,))
            row = await cursor.fetchone()
            if row:
                raise HTTPException(404, "phone number already exists")

        await db.execute(f"""
        UPDATE {Tables.users} SET 
            name = ?, 
            phone = ?, 
            age = ?
        WHERE id = ?""", (
            body.name,
            body.phone,
            body.age,
            id
        ))
        await db.commit()

        return {"message": "user updated"}
    
@router.put("/photo", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def edit_user_photo(id: int, file: UploadFile = File(...)):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.users} WHERE id = ?", (id,))
        row = await cursor.fetchone()
        if not row:
            raise HTTPException(404, "user not found")

        format = str(file.filename).split('.')[-1]
        if format not in settings.image_formats:
            raise HTTPException(400, 'file error')

        key = f"users/{id}.{format}"
        url = f"{settings.endpoint_url}/{settings.Bucket}/{key}"

        await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.png")
        await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.jpg")
        await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.jpeg")

        await s3.put_object(
            Bucket=settings.Bucket,
            Key=key,
            Body=await file.read(),
            ContentType=file.content_type,
        )

        await db.execute(
            f"UPDATE {Tables.users} SET photo = ? WHERE id = ?",
            (url, id),
        )
        await db.commit()

        return {"message": "user photo updated"}

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_user(id: int):
    async with get_db() as db:        
        await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.png")
        await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.jpg")
        await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.jpeg")

        await db.execute(f"DELETE FROM {Tables.users} WHERE id = ?", (id,))
        await db.commit()

        return {"message": "user deleted"}
