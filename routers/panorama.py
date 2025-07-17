from fastapi       import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic      import BaseModel
from core.db       import Tables, get_db
from core.security import JWTBearer, Roles
from core.settings import settings, s3

router = APIRouter()

class PanoramaModel(BaseModel):
    url: str
    rid: int

@router.get("/")
async def get_panoramas(rid: int):
    async with get_db() as db:
        cursor = await db.execute(f"SELECT * FROM {Tables.panoramas} WHERE rid = ?", (rid,))
        rows = await cursor.fetchall()

        return {"panoramas": [dict(row) for row in rows]}

# @router.post("/")
# async def add_panorama(rid: int, file: UploadFile = File()):
#     async with get_db() as db:
#         cursor = await db.execute(f"SELECT * FROM {Tables.restaurants} WHERE id = ?", (rid,))
#         row = await cursor.fetchone()
#         if not row:
#             raise HTTPException(404, "restaurant not found")

#         format = str(file.filename).split('.')[-1]
#         if format not in settings.image_formats:
#             raise HTTPException(400, 'file error')

#         key = f"panoramas/{rid}.{format}"
#         url = f"{settings.endpoint_url}/{settings.Bucket}/{key}"

#         await s3.put_object(
#             Bucket=settings.Bucket,
#             Key=key,
#             Body=await file.read(),
#             ContentType=file.content_type,
#         )

#         await db.execute(f"""
#             INSERT INTO {Tables.panoramas} (url, rid)
#             VALUES (?, ?)
#         """, (url, rid))
#         await db.commit()

#         return {"message": "panorama added"}

# @router.put("/photo")
# async def edit_user_photo(id: int, file: UploadFile = File()):
#     async with get_db() as db:
#         cursor = await db.execute(f"SELECT * FROM {Tables.users} WHERE id = ?", (id,))
#         row = await cursor.fetchone()
#         if not row:
#             raise HTTPException(404, "user not found")

#         format = str(file.filename).split('.')[-1]
#         if format not in settings.image_formats:
#             raise HTTPException(400, 'file error')

#         key = f"users/{id}.{format}"
#         url = f"{settings.endpoint_url}/{settings.Bucket}/{key}"

#         await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.png")
#         await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.jpg")
#         await s3.delete_object(Bucket=settings.Bucket, Key=f"users/{id}.jpeg")

#         await s3.put_object(
#             Bucket=settings.Bucket,
#             Key=key,
#             Body=await file.read(),
#             ContentType=file.content_type,
#         )

#         await db.execute(
#             f"UPDATE {Tables.users} SET photo = ? WHERE id = ?",
#             (url, id),
#         )
#         await db.commit()

#         return {"message": "user photo updated"}

# , dependencies=[Depends(JWTBearer(role=Roles.user))]