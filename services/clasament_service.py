from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from services.database import AsyncSessionLocal
from models.user_model import User
from models.referral_model import Referral
from datetime import datetime, timedelta

class ClasamentService:
    async def get_leaderboard(self, range_type: str, page: int = 1, per_page: int = 10):
        async with AsyncSessionLocal() as session:
            offset = (page - 1) * per_page
            
            # Base query
            if range_type == "all":
                # All-time leaderboard
                query = select(
                    User.username,
                    User.xp_total,
                    func.count(Referral.id).label('qualified_referrals')
                ).outerjoin(
                    Referral, and_(
                        Referral.inviter_id == User.id,
                        Referral.status == "qualified"
                    )
                ).group_by(User.id, User.username, User.xp_total)
                
            elif range_type in ["7", "30"]:
                # Time-based leaderboard
                days = int(range_type)
                cutoff_date = datetime.now() - timedelta(days=days)
                
                query = select(
                    User.username,
                    User.xp_total,
                    func.count(Referral.id).label('qualified_referrals')
                ).outerjoin(
                    Referral, and_(
                        Referral.inviter_id == User.id,
                        Referral.status == "qualified",
                        Referral.qualified_at >= cutoff_date
                    )
                ).group_by(User.id, User.username, User.xp_total)
            
            # Order by qualified referrals desc, then XP desc, then joined_at asc
            query = query.order_by(
                desc('qualified_referrals'),
                desc(User.xp_total),
                User.joined_at
            ).offset(offset).limit(per_page)
            
            result = await session.execute(query)
            return [
                {
                    'username': row.username,
                    'xp_total': row.xp_total,
                    'qualified_referrals': row.qualified_referrals
                }
                for row in result
            ]
    
    async def get_user_position(self, tg_id: int, range_type: str):
        async with AsyncSessionLocal() as session:
            # Get user data first
            user_result = await session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return None
            
            # Get user's qualified referrals count for the range
            if range_type == "all":
                user_refs_result = await session.execute(
                    select(func.count(Referral.id)).where(
                        Referral.inviter_id == user.id,
                        Referral.status == "qualified"
                    )
                )
            else:
                days = int(range_type)
                cutoff_date = datetime.now() - timedelta(days=days)
                user_refs_result = await session.execute(
                    select(func.count(Referral.id)).where(
                        Referral.inviter_id == user.id,
                        Referral.status == "qualified",
                        Referral.qualified_at >= cutoff_date
                    )
                )
            
            user_refs = user_refs_result.scalar() or 0
            
            # Count users with better stats
            if range_type == "all":
                better_users_query = select(func.count(User.id)).select_from(
                    select(
                        User.id,
                        func.count(Referral.id).label('qualified_referrals')
                    ).outerjoin(
                        Referral, and_(
                            Referral.inviter_id == User.id,
                            Referral.status == "qualified"
                        )
                    ).group_by(User.id).subquery()
                ).where(
                    # Better referrals count, or same referrals but better XP, or same both but earlier join
                    func.coalesce(func.count(Referral.id), 0) > user_refs
                )
            else:
                days = int(range_type)
                cutoff_date = datetime.now() - timedelta(days=days)
                better_users_query = select(func.count(User.id)).select_from(
                    select(
                        User.id,
                        func.count(Referral.id).label('qualified_referrals')
                    ).outerjoin(
                        Referral, and_(
                            Referral.inviter_id == User.id,
                            Referral.status == "qualified",
                            Referral.qualified_at >= cutoff_date
                        )
                    ).group_by(User.id).subquery()
                ).where(
                    func.coalesce(func.count(Referral.id), 0) > user_refs
                )
            
            better_count_result = await session.execute(better_users_query)
            better_count = better_count_result.scalar() or 0
            
            return better_count + 1

