from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from services.database import AsyncSessionLocal
from models.user_model import User
from models.referral_model import Referral
from models.xp_event_model import XPEvent
from datetime import datetime
import hashlib

class ReferralService:
    async def get_or_create_referral_code(self, tg_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return None
            
            if not user.referral_code:
                # Generate referral code
                code_hash = hashlib.md5(str(tg_id).encode()).hexdigest()[:8]
                referral_code = f"ref_{tg_id}_{code_hash}"
                
                await session.execute(
                    update(User).where(User.tg_id == tg_id).values(referral_code=referral_code)
                )
                await session.commit()
                return referral_code
            
            return user.referral_code
    
    async def get_referral_stats(self, tg_id: int):
        async with AsyncSessionLocal() as session:
            # Get user ID
            result = await session.execute(
                select(User.id).where(User.tg_id == tg_id)
            )
            user_id = result.scalar_one_or_none()
            
            if not user_id:
                return {"total": 0, "qualified": 0, "pending": 0}
            
            # Get total referrals
            total_result = await session.execute(
                select(func.count(Referral.id)).where(Referral.inviter_id == user_id)
            )
            total = total_result.scalar() or 0
            
            # Get qualified referrals
            qualified_result = await session.execute(
                select(func.count(Referral.id)).where(
                    Referral.inviter_id == user_id,
                    Referral.status == "qualified"
                )
            )
            qualified = qualified_result.scalar() or 0
            
            # Get pending referrals
            pending_result = await session.execute(
                select(func.count(Referral.id)).where(
                    Referral.inviter_id == user_id,
                    Referral.status == "pending"
                )
            )
            pending = pending_result.scalar() or 0
            
            return {
                "total": total,
                "qualified": qualified,
                "pending": pending
            }
    
    async def process_referral(self, referral_code: str, invited_tg_id: int):
        """Process a referral when someone joins via referral link"""
        async with AsyncSessionLocal() as session:
            # Get inviter by referral code
            inviter_result = await session.execute(
                select(User).where(User.referral_code == referral_code)
            )
            inviter = inviter_result.scalar_one_or_none()
            
            if not inviter:
                return False
            
            # Get invited user
            invited_result = await session.execute(
                select(User).where(User.tg_id == invited_tg_id)
            )
            invited = invited_result.scalar_one_or_none()
            
            if not invited:
                return False
            
            # Check if already referred
            existing_result = await session.execute(
                select(Referral).where(Referral.invited_id == invited.id)
            )
            existing = existing_result.scalar_one_or_none()
            
            if existing:
                return False  # Already referred
            
            # Create referral record
            referral = Referral(
                inviter_id=inviter.id,
                invited_id=invited.id,
                link_code=referral_code,
                status="pending"
            )
            session.add(referral)
            
            # Update invited user's invited_by
            await session.execute(
                update(User).where(User.id == invited.id).values(invited_by=inviter.id)
            )
            
            await session.commit()
            return True
    
    async def qualify_referral(self, invited_tg_id: int):
        """Qualify a referral when the invited user joins the group"""
        async with AsyncSessionLocal() as session:
            # Get invited user
            invited_result = await session.execute(
                select(User).where(User.tg_id == invited_tg_id)
            )
            invited = invited_result.scalar_one_or_none()
            
            if not invited:
                return False
            
            # Get referral record
            referral_result = await session.execute(
                select(Referral).where(
                    Referral.invited_id == invited.id,
                    Referral.status == "pending"
                )
            )
            referral = referral_result.scalar_one_or_none()
            
            if not referral:
                return False
            
            # Update referral status
            await session.execute(
                update(Referral).where(Referral.id == referral.id).values(
                    status="qualified",
                    qualified_at=datetime.now()
                )
            )
            
            # Award XP to inviter
            xp_event = XPEvent(
                user_id=referral.inviter_id,
                type="referral_qualified",
                delta=100,
                meta_json=f'{{"invited_user_id": {invited.id}}}'
            )
            session.add(xp_event)
            
            # Update inviter's XP and rank
            inviter_result = await session.execute(
                select(User).where(User.id == referral.inviter_id)
            )
            inviter = inviter_result.scalar_one_or_none()
            
            if inviter:
                new_xp = inviter.xp_total + 100
                new_rank = self._calculate_rank(await self._get_qualified_referrals_count(referral.inviter_id))
                
                await session.execute(
                    update(User).where(User.id == referral.inviter_id).values(
                        xp_total=new_xp,
                        rank_level=new_rank
                    )
                )
            
            await session.commit()
            return True
    
    async def _get_qualified_referrals_count(self, user_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(func.count(Referral.id)).where(
                    Referral.inviter_id == user_id,
                    Referral.status == "qualified"
                )
            )
            return result.scalar() or 0
    
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

