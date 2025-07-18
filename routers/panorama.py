from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from core.security import JWTBearer, Roles
from core.schemas import Panorama
from core.settings import settings, s3
from core.db import (
    db_get_panoramas,
)

router = APIRouter()

@router.get("/")
async def get_panoramas(rid: int):
    rows = await db_get_panoramas(rid)

    return {
        "rid": rid,
        "panoramas": rows,
    }
