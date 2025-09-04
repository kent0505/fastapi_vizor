from fastapi import APIRouter
from api.v1.auth import router as auth_router
from api.v1.client import router as client_router
from api.v1.user import router as user_router
from api.v1.admin import router as admin_router
from api.v1.city import router as city_router
from api.v1.restaurant import router as restaurant_router
from api.v1.panorama import router as panorama_router
from api.v1.table import router as table_router
from api.v1.hotspot import router as hotspot_router
from api.v1.category import router as category_router
from api.v1.menu import router as menu_router
from api.v1.flower import router as flower_router
from api.v1.flower_order import router as flower_order_router

router = APIRouter()

router.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
router.include_router(client_router, prefix="/api/v1/client", tags=["Client"])
router.include_router(user_router, prefix="/api/v1/user", tags=["User"])
router.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])
router.include_router(city_router, prefix="/api/v1/city", tags=["City"])
router.include_router(restaurant_router, prefix="/api/v1/restaurant", tags=["Restaurant"])
router.include_router(panorama_router, prefix="/api/v1/panorama", tags=["Panorama"])
router.include_router(table_router, prefix="/api/v1/table", tags=["Table"])
router.include_router(hotspot_router, prefix="/api/v1/hotspot", tags=["Hotspot"])
router.include_router(category_router, prefix="/api/v1/category", tags=["Category"])
router.include_router(menu_router, prefix="/api/v1/menu", tags=["Menu"])
router.include_router(flower_router, prefix="/api/v1/flower", tags=["Flower"])
router.include_router(flower_order_router, prefix="/api/v1/flower_order", tags=["Flower Order"])
