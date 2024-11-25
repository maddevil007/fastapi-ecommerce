from pydantic import BaseModel, EmailStr

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserResponseSchema(BaseModel):
    email: EmailStr
    name: str
    role: str
