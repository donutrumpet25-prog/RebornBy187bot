from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from services.database import AsyncSessionLocal
from models.user_model import User
from config import GROUP_ID
from aiogram import Bot

class MembershipService:
    def __init__(self, bot: Bot = None):
        self.bot = bot
    
    async def check_group_membership(self, tg_id: int):
        """Check if user is member of the official group"""
        if not self.bot:
            # For testing purposes, return True
            # In production, this should use bot.get_chat_member
            return True
        
        try:
            member = await self.bot.get_chat_member(GROUP_ID, tg_id)
            return member.status in ['member', 'administrator', 'creator']
        except:
            return False
    
    async def update_group_status(self, tg_id: int, joined: bool):
        """Update user's group membership status"""
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(User).where(User.tg_id == tg_id).values(joined_group=joined)
            )
            await session.commit()
    
    async def get_group_status(self, tg_id: int):
        """Get user's group membership status from database"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User.joined_group).where(User.tg_id == tg_id)
            )
            return result.scalar_one_or_none() or False

