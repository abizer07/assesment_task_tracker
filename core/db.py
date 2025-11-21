from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,          # ← verify connection is alive
    pool_recycle=300,            # ← recycle after 5 min ( < 60 s )
    connect_args={"ssl": "require"},
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
