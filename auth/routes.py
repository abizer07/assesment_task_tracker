from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserResponseSchema,
    TokenSchema
)
from .services import (
    user_register_service,
    user_login_service,
)

from core.db import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponseSchema)
async def register_user_api(
    payload: UserRegisterSchema,
    db: AsyncSession = Depends(get_db)
):
    print(f"{payload=}")
    user = await user_register_service(payload, db)
    return user


@router.post("/login", response_model=TokenSchema)
async def login_user_api(
    payload: UserLoginSchema,
    db: AsyncSession = Depends(get_db)
):
    print(f"{payload}")
    token = await user_login_service(payload, db)
    return {"access_token": token, "token_type": "bearer"}
