from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from services.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    verified = Column(Boolean, default=False)
    warns = Column(Integer, default=0)
    conflicts = Column(Integer, default=0)
    reputation = Column(Integer, default=0)
    xp_total = Column(Integer, default=0)
    rank_level = Column(Integer, default=0)
    grade = Column(String, nullable=True)
    referral_code = Column(String, unique=True, nullable=True)
    joined_group = Column(Boolean, default=False)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True)


