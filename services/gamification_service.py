from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from services.database import AsyncSessionLocal
from models.user_model import User
from models.xp_event_model import XPEvent
from datetime import datetime

class GamificationService:
    async def award_xp(self, user_id: int, xp_type: str, delta: int, meta_json: str = None):
        """Award XP to a user and update their total"""
        async with AsyncSessionLocal() as session:
            # Create XP event
            xp_event = XPEvent(
                user_id=user_id,
                type=xp_type,
                delta=delta,
                meta_json=meta_json
            )
            session.add(xp_event)
            
            # Update user's total XP
            user_result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = user_result.scalar_one_or_none()
            
            if user:
                new_xp = user.xp_total + delta
                await session.execute(
                    update(User).where(User.id == user_id).values(xp_total=new_xp)
                )
            
            await session.commit()
            return True
    
    async def award_weekly_loyalty_xp(self):
        """Award weekly loyalty XP to all users"""
        async with AsyncSessionLocal() as session:
            # Get all users
            users_result = await session.execute(select(User))
            users = users_result.scalars().all()
            
            for user in users:
                # Award 10 XP for weekly loyalty
                xp_event = XPEvent(
                    user_id=user.id,
                    type="weekly_loyalty",
                    delta=10,
                    meta_json='{"week": "' + datetime.now().strftime("%Y-W%U") + '"}'
                )
                session.add(xp_event)
                
                # Update user's total XP
                new_xp = user.xp_total + 10
                await session.execute(
                    update(User).where(User.id == user.id).values(xp_total=new_xp)
                )
            
            await session.commit()
    
    async def verify_user(self, user_id: int):
        """Verify a user and award verification XP"""
        async with AsyncSessionLocal() as session:
            # Update user verification status
            await session.execute(
                update(User).where(User.id == user_id).values(verified=True)
            )
            
            # Award verification XP
            await self.award_xp(user_id, "verify_full", 100, '{"verification": "full"}')
            
            await session.commit()
            return True

