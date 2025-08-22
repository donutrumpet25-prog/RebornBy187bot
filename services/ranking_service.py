from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from services.database import AsyncSessionLocal
from models.user_model import User
from models.referral_model import Referral

class RankingService:
    async def get_user_progress(self, tg_id: int):
        async with AsyncSessionLocal() as session:
            # Get user data
            user_result = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return None
            
            # Get qualified referrals count
            referrals_result = await session.execute(
                select(func.count(Referral.id)).where(
                    Referral.inviter_id == user.id,
                    Referral.status == "qualified"
                )
            )
            qualified_referrals = referrals_result.scalar() or 0
            
            return {
                "rank_level": user.rank_level,
                "qualified_referrals": qualified_referrals,
                "xp_total": user.xp_total,
                "grade": user.grade
            }
    
    async def update_user_rank(self, user_id: int, qualified_referrals: int):
        """Update user rank based on qualified referrals"""
        new_rank = self._calculate_rank(qualified_referrals)
        
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(User).where(User.id == user_id).values(rank_level=new_rank)
            )
            await session.commit()
            return new_rank
    
    def _calculate_rank(self, qualified_referrals: int):
        """Calculate rank based on qualified referrals"""
        if qualified_referrals >= 100:
            return 5  # Hustler (VIP)
        elif qualified_referrals >= 50:
            return 4  # Connector
        elif qualified_referrals >= 25:
            return 3  # Support
        elif qualified_referrals >= 20:
            return 2  # Aspirant
        elif qualified_referrals >= 15:
            return 1  # Inițiat
        else:
            return 0  # Începător

