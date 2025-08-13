from fastapi import APIRouter
from db import SessionDep, BaseModel

router = APIRouter()

class PanoramaBody(BaseModel):
    rid: int
    photo: str

# @router.post("/")
# async def add_panorama(rid: int, file: UploadFile = File()):
#     row = await db_get_by_id(Restaurant, Tables.restaurants, rid)
#     if not row:
#         raise HTTPException(404, "restaurant not found")

#     format = get_format(str(file.filename))
#     if format not in settings.image_formats:
#         raise HTTPException(400, 'file error')

#     key = f"panoramas/{get_timestamp()}.{format}"

#     await put_object(key, file)

#     await db_add_panorama(key, rid)

#     return {"message": "panorama added"}

# @router.delete("/")
# async def delete_panorama(id: int):
#     row = await db_get_by_id(Panorama, Tables.panoramas, id)
#     if not row:
#         raise HTTPException(404, "panorama not found")

#     parsed_url = urlparse(row.photo)
#     path = parsed_url.path
#     filename = os.path.basename(path)

#     await delete_object(f"panoramas/{filename}")

#     await db_delete(Tables.panoramas, id)

#     return {"message": "panorama deleted"}
