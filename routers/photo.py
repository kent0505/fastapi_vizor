from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer, Roles
from core.s3 import put_object, delete_object
from db.user import db_get_user_by_id

router = APIRouter()

@router.post("/user", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def add_user_photo(
    id: int, 
    file: UploadFile = File(),
):
    row = await db_get_user_by_id(id)
    if not row:
        raise HTTPException(404, "user not found")
    
    key = f"users/{id}"

    photo = await put_object(key, file)

    return {
        "message": "user photo added",
        "photo": photo,
    }

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_photo(key: str):
    await delete_object(key)

    return {"message": "photo deleted"}
