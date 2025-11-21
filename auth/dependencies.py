from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import get_db
from auth.services import get_user_by_id


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Read Authorization header
    auth_header = request.headers.get("Authorization")
    print(f"{auth_header=}")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )

    token = auth_header.split(" ")[1]
    print(f"{token=}")

    try:
        # Decode JWT with correct settings keys
        payload = jwt.decode(
            token,
            settings.secret_key,        # FIXED
            algorithms=[settings.algorithm],   # FIXED
        )

        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # Fetch user from DB
        user = await get_user_by_id(user_id)   # FIXED: pass db
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
