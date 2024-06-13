from fastapi import APIRouter
from models.Users import User
from jwt_man import create_token
from fastapi.responses import JSONResponse

user_router = APIRouter()

@user_router.post('/login', tags=['Aunth'])
def login(user: User):
    if user.email == "admin" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content = token)
    return user