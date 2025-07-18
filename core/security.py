from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from core.settings import settings
from dataclasses import dataclass

import jwt

@dataclass
class Roles:
    admin: str = "admin"
    user: str = "user"

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
        },
        key=settings.jwt_key,
        algorithm="HS256",
    )

class JWTBearer(HTTPBearer):
    def __init__(
        self, 
        role: str = Roles.admin
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
                key=settings.jwt_key,
                algorithms=["HS256"],
            )
        except ExpiredSignatureError:
            raise HTTPException(403, "Token has expired.")
        except InvalidTokenError:
            raise HTTPException(403, "Invalid token.")
        except:
            raise HTTPException(403, "Invalid error.")
        if payload.get("role") not in [self.role, Roles.admin]:
            raise HTTPException(403, "Access denied for this role.")

        return token.credentials
