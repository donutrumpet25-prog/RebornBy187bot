from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from services.database import AsyncSessionLocal
from models.user_model import User
from models.referral_model import Referral

class ProfileService:
    async def get_user_profile(self, tg_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
    
    async def get_referral_count(self, user_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(func.count(Referral.id)).where(
                    Referral.inviter_id == user_id,
                    Referral.status == "qualified"
                )
            )
            return result.scalar() or 0
    
    async def create_or_update_user(self, tg_id: int, username: str = None, first_name: str = None):
        async with AsyncSessionLocal() as session:
            # Check if user exists
            result = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                # Create new user
                user = User(
                    tg_id=tg_id,
                    username=username,
                    first_name=first_name,
                    referral_code=f"ref_{tg_id}_{hash(str(tg_id)) % 10000}"
                )
                session.add(user)
            else:
                # Update existing user
                user.username = username
                user.first_name = first_name
            
            await session.commit()
            await session.refresh(user)
            return user

