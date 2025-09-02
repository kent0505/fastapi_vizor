from pydantic import BaseModel
from db import Base, Mapped, mapped_column
from core.security import Roles

class User(Base):
    phone: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(default=Roles.user.value) # admin, stuff, user
    code: Mapped[str] = mapped_column(nullable=True)
    fcm: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)

class UserSchema(BaseModel):
    phone: str
    name: str
    age: str

class UserEditSchema(BaseModel):
    name: str
    age: str
    fcm: str

class AdminSchema(BaseModel):
    name: str = "Otabek"
    phone: str = "+998998472580"

class PhoneSchema(BaseModel):
    phone: str = "+998998472580"

class LoginSchema(BaseModel):
    phone: str = "+998998472580"
    code: str
