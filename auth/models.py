from sqlalchemy import Column, Integer, String
from core.db import Base   # ✅ Use global Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200))
    email = Column(String(200), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
