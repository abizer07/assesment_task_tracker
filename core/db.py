from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import settings

Base = declarative_base()

# ✅ Use settings.database_url (lowercase)
engine = create_async_engine(
    settings.database_url,
    echo=True
)

# Session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency
async def get_db():
    async with async_session() as session:
        yield session
