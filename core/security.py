from fastapi          import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt              import ExpiredSignatureError, InvalidTokenError
from core.settings    import settings

import jwt

def signJWT(
    id:   int, 
    role: str, 
    exp:  int,
) -> str:
    return jwt.encode(
        {
            "id":   id,
            "role": role,
            "exp":  exp,
        },
        key=settings.jwt_key,
        algorithm="HS256"
    )

class JWTBearer(HTTPBearer):
    def __init__(
        self, 
        auto_error: bool = True, 
        role: str = settings.user # default role is 'user'
    ):
        super().__init__(auto_error=auto_error)
        self.role = role

    async def __call__(self, request: Request):
        token: HTTPAuthorizationCredentials = await super().__call__(request)

        if token.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

        try:
            payload: dict = jwt.decode(
                jwt=token.credentials,
                key=settings.jwt_key,
                algorithms=["HS256"]
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token has expired.")
        except InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid token.")
        except:
            raise HTTPException(status_code=403, detail="Invalid error.")
        if payload.get("role") not in [self.role, settings.admin]:
            raise HTTPException(status_code=403, detail="Access denied for this role.")
        # if payload.get("role") != self.role:
        #     raise HTTPException(status_code=403, detail="Invalid role.")
        return token.credentials
