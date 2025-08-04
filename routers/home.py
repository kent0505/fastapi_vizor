from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.security import Roles
from core.settings import settings
from core.utils import hash_password
from db.user import (
    User,
    db_get_users,
    db_add_user,
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    users = await db_get_users()
    if not users:
        password: str = hash_password(settings.password)
        await db_add_user(
            role=Roles.admin,
            user=User(
                name="Otabek",
                phone="+998998472580",
                password=password,
                age=25,
            ),
        )
        users = await db_get_users()

    # restaurants = await db_get_list(Tables.restaurants)
    # panoramas = await db_get_list(Tables.panoramas)
    # hotspots = await db_get_list(Tables.hotspots)
    # menus = await db_get_list(Tables.menus)

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            # "restaurants": restaurants,
            # "panoramas": panoramas,
            # "hotspots": hotspots,
            # "menus": menus,
        }
    )
