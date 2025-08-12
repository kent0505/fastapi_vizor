from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from enum import Enum
from core.config import settings

import jwt

class Roles(str, Enum):
    admin = "admin"
    stuff = "stuff"
    user = "user"

def signJWT(
    id: int, 
    role: str, 
    exp: int,
) -> str:
    return jwt.encode(
        {
            "id": id,
            "role": role,
            "exp": exp,
            "version": settings.version,
        },
        key=settings.token,
        algorithm="HS256",
    )

class JWTBearer(HTTPBearer):
    def __init__(
        self, 
        role: str = Roles.admin,
    ):
        super().__init__(auto_error=True)
        self.role = role

    async def __call__(self, request: Request):
        token: HTTPAuthorizationCredentials = await super().__call__(request)

        if token.scheme != "Bearer":
            raise HTTPException(403, "Invalid authentication scheme.")

        try:
            payload: dict = jwt.decode(
                jwt=token.credentials,
                key=settings.token,
                algorithms=["HS256"],
            )
        except ExpiredSignatureError:
            raise HTTPException(403, "Token has expired.")
        except InvalidTokenError:
            raise HTTPException(403, "Invalid token.")
        except:
            raise HTTPException(403, "Invalid error.")

        if self.role == Roles.user:
            allowed_roles = [Roles.user, Roles.stuff, Roles.admin]
        else:
            allowed_roles = [self.role, Roles.admin]

        if payload.get("role") not in allowed_roles:
            raise HTTPException(403, "Access denied for this role.")

        if payload.get("version") != settings.version:
            raise HTTPException(403, "Token version mismatch.")

        return token.credentials
