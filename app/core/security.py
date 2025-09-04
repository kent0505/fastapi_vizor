from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from typing import Annotated
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
            "version": settings.jwt.version,
        },
        key=settings.jwt.key,
        algorithm=settings.jwt.algorithm,
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
            raise HTTPException(403, "invalid authentication scheme")

        try:
            payload: dict = jwt.decode(
                jwt=token.credentials,
                key=settings.jwt.key,
                algorithms=[settings.jwt.algorithm],
            )
        except ExpiredSignatureError:
            raise HTTPException(403, "token has expired")
        except InvalidTokenError:
            raise HTTPException(403, "invalid token")
        except:
            raise HTTPException(403, "auth error")

        if self.role == Roles.user:
            allowed_roles = [Roles.user, Roles.stuff, Roles.admin]
        else:
            allowed_roles = [self.role, Roles.admin]

        if payload.get("role") not in allowed_roles:
            raise HTTPException(403, "access denied for this role")

        if payload.get("version") != settings.jwt.version:
            raise HTTPException(403, "token version mismatch")

        return payload.get("id")

UserDep = Annotated[int, Depends(JWTBearer(role=Roles.user))]
