from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_service import register_user, login_user
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema

auth_router = APIRouter()

@auth_router.post("/signup", response_model=dict)
async def signup(user: UserCreateSchema):
    response = await register_user(user.email, user.password, user.name)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response

@auth_router.post("/login", response_model=dict)
async def login(email: str, password: str):
    response = await login_user(email, password)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return response
