from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    email: EmailStr
    hashed_password: str
    name: str
    role: str = "customer"  # Default role
