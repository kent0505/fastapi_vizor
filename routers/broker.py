from faststream.rabbit.fastapi import RabbitRouter
from core.config               import settings

router = RabbitRouter(url=settings.rabbit_url)

@router.post("/order")
async def test(name: str):
    await router.broker.publish(
        f"New orders: {name}",
        queue="orders",
    )
    return {"message": "OK"}
