from db import (
    BaseModel,
    Optional,
)

class Menu(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    category: str
    photo: Optional[str] = None
    price: str
    rid: int
