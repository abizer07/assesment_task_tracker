from pydantic import BaseModel, EmailStr

class UserRegisterSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
