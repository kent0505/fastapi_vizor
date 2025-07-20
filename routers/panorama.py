from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer, Roles
from urllib.parse import urlparse
from core.settings import settings
from core.s3 import delete_object, put_object
from core.utils import get_format, get_timestamp
from core.db import (
    db_get_panoramas_by_rid,
    db_get_panorama_by_id,
    db_add_panorama,
    db_get_restaurant_by_id,
    db_delete_panorama
)

import os

router = APIRouter()

@router.get("/", dependencies=[Depends(JWTBearer(role=Roles.user))])
async def get_panoramas(rid: int):
    rows = await db_get_panoramas_by_rid(rid)

    return {
        "rid": rid,
        "panoramas": rows,
    }

@router.post("/", dependencies=[Depends(JWTBearer())])
async def add_panorama(rid: int, file: UploadFile = File()):
    row = await db_get_restaurant_by_id(rid)
    if not row:
        raise HTTPException(404, "restaurant not found")

    format = get_format(str(file.filename))
    if format not in settings.image_formats:
        raise HTTPException(400, 'file error')

    key = f"panoramas/{get_timestamp()}.{format}"

    await put_object(key, file)

    await db_add_panorama(key, rid)

    return {"message": "panorama added"}

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def delete_panorama(id: int):
    row = await db_get_panorama_by_id(id)
    if not row:
        raise HTTPException(404, "panorama not found")

    parsed_url = urlparse(row.photo)
    path = parsed_url.path
    filename = os.path.basename(path)

    await delete_object(f"panoramas/{filename}")

    await db_delete_panorama(id)

    return {"message": "panorama deleted"}
