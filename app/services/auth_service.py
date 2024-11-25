from passlib.context import CryptContext
from app.db import users_collection
from app.utils.jwt_handler import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def register_user(email: str, password: str, name: str):
    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        return {"error": "User already exists"}
    
    hashed_password = await hash_password(password)
    user = {"email": email, "hashed_password": hashed_password, "name": name, "role": "customer"}
    await users_collection.insert_one(user)
    return {"message": "User registered successfully"}

async def login_user(email: str, password: str):
    user = await users_collection.find_one({"email": email})
    if not user or not await verify_password(password, user["hashed_password"]):
        return {"error": "Invalid credentials"}
    
    token = create_access_token({"sub": email})
    return {"access_token": token, "token_type": "bearer"}
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
