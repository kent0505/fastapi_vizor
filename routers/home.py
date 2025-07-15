from fastapi            import APIRouter, Request
from fastapi.templating import Jinja2Templates
from core.db            import Tables, get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request):
    async with get_db() as db:
        user_cursor = await db.execute(f"SELECT * FROM {Tables.users}")
        users = await user_cursor.fetchall()

        restaurant_cursor = await db.execute(f"SELECT * FROM {Tables.restaurants}")
        restaurants = await restaurant_cursor.fetchall()

    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "users": users,
            "restaurants": [dict(row) for row in restaurants],
        }
    )
