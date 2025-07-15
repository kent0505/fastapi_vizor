from fastapi            import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.db            import Tables, get_db
from datetime           import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    async with get_db() as db:
        user_cursor = await db.execute(f"SELECT * FROM {Tables.users}")
        users_raw = await user_cursor.fetchall()

        restaurant_cursor = await db.execute(f"SELECT * FROM {Tables.restaurants}")
        restaurants_raw = await restaurant_cursor.fetchall()

    users = []
    for row in users_raw:
        user = dict(row)
        user["date"] = datetime.fromtimestamp(user["date"]).strftime("%d.%m.%Y %H:%M:%S")
        users.append(user)

    restaurants = [dict(row) for row in restaurants_raw]

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            "restaurants": restaurants,
        }
    )
