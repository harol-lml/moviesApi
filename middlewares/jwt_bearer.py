from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_man import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        aunth = await super().__call__(request)
        data = validate_token(aunth.credentials)
        if data['email'] != "admin":
            raise HTTPException(status_code=403, detail="Invalid credentials")