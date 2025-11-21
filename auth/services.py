from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
import jwt
from core.config import settings


from .models import UserModel
from .schemas import UserRegisterSchema, UserLoginSchema

# Fixed: Configure passlib with proper bcrypt settings
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b"
)

SECRET_KEY =settings.secret_key       # TODO: Load from env
ALGORITHM = settings.algorithm


# -------------------------
# Password Handling
# -------------------------
def safe_bcrypt_hash(password: str) -> str:
    """
    Safely hash password for bcrypt by encoding to bytes and truncating.
    Handles both ASCII and Unicode characters properly.
    """
    # Encode to UTF-8 bytes and truncate to 72 bytes
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    # Convert back to string for passlib (it will encode again internally)
    return pwd_context.hash(password_bytes.decode('utf-8', 'ignore'))


def safe_bcrypt_verify(raw_password: str, hashed_password: str) -> bool:
    """
    Safely verify password against bcrypt hash.
    """
    raw_bytes = raw_password.encode('utf-8')
    if len(raw_bytes) > 72:
        raw_bytes = raw_bytes[:72]
    return pwd_context.verify(raw_bytes.decode('utf-8', 'ignore'), hashed_password)


# -------------------------
# JWT Creator
# -------------------------
def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=12)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------
# Register Service
# -------------------------
async def user_register_service(
    data: UserRegisterSchema,
    db: AsyncSession
):
    # Check if email exists
    stmt = select(UserModel).where(UserModel.email == data.email)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = UserModel(
        full_name=data.full_name,
        email=data.email,
        # password=safe_bcrypt_hash(data.password)
        password=data.password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


# -------------------------
# Login Service
# -------------------------
async def user_login_service(
    data: UserLoginSchema,
    db: AsyncSession
):
    stmt = select(UserModel).where(UserModel.email == data.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # if not safe_bcrypt_verify(data.password, user.password):
    if data.password != user.password :
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_jwt_token({"user_id": user.id})
    return token

from core.db import async_session
from sqlalchemy.future import select

async def get_user_by_id(user_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()
