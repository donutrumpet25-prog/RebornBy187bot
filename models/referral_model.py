from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from services.database import Base

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invited_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    link_code = Column(String, nullable=False)
    status = Column(String, default="pending") # enum pending/qualified/rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    qualified_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (UniqueConstraint("invited_id"),)


