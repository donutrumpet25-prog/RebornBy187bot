from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from services.database import AsyncSessionLocal
from models.user_model import User
from models.seller_model import Seller
from models.product_model import Product
from models.location_model import Location
from models.seller_product_model import SellerProduct
from models.transaction_model import Transaction
from models.xp_event_model import XPEvent
from datetime import datetime

class AdminService:
    async def add_seller(self, username: str):
        async with AsyncSessionLocal() as session:
            # Find user by username
            user_result = await session.execute(
                select(User).where(User.username == username)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return False
            
            # Check if already a seller
            seller_result = await session.execute(
                select(Seller).where(Seller.user_id == user.id)
            )
            existing_seller = seller_result.scalar_one_or_none()
            
            if existing_seller:
                # Reactivate if inactive
                if not existing_seller.is_active:
                    await session.execute(
                        update(Seller).where(Seller.id == existing_seller.id).values(is_active=True)
                    )
                    await session.commit()
                return True
            
            # Create new seller
            seller = Seller(
                user_id=user.id,
                display_name=user.first_name or user.username,
                is_active=True
            )
            session.add(seller)
            await session.commit()
            return True
    
    async def remove_seller(self, username: str):
        async with AsyncSessionLocal() as session:
            # Find user by username
            user_result = await session.execute(
                select(User).where(User.username == username)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return False
            
            # Find seller
            seller_result = await session.execute(
                select(Seller).where(Seller.user_id == user.id)
            )
            seller = seller_result.scalar_one_or_none()
            
            if not seller:
                return False
            
            # Deactivate seller and remove mappings
            await session.execute(
                update(Seller).where(Seller.id == seller.id).values(is_active=False)
            )
            
            # Remove product mappings
            await session.execute(
                delete(SellerProduct).where(SellerProduct.seller_id == seller.id)
            )
            
            await session.commit()
            return True
    
    async def set_seller_location(self, username: str, sector_number: int):
        async with AsyncSessionLocal() as session:
            # Find user
            user_result = await session.execute(
                select(User).where(User.username == username)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return False
            
            # Find seller
            seller_result = await session.execute(
                select(Seller).where(Seller.user_id == user.id)
            )
            seller = seller_result.scalar_one_or_none()
            
            if not seller:
                return False
            
            # Find location by sector
            location_result = await session.execute(
                select(Location).where(Location.sector_number == sector_number)
            )
            location = location_result.scalar_one_or_none()
            
            if not location:
                return False
            
            # Update seller location
            await session.execute(
                update(Seller).where(Seller.id == seller.id).values(location_id=location.id)
            )
            await session.commit()
            return True
    
    async def set_seller_products(self, username: str, product_names: list):
        async with AsyncSessionLocal() as session:
            # Find user
            user_result = await session.execute(
                select(User).where(User.username == username)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return False
            
            # Find seller
            seller_result = await session.execute(
                select(Seller).where(Seller.user_id == user.id)
            )
            seller = seller_result.scalar_one_or_none()
            
            if not seller:
                return False
            
            # Remove existing product mappings
            await session.execute(
                delete(SellerProduct).where(SellerProduct.seller_id == seller.id)
            )
            
            # Add new product mappings
            for product_name in product_names:
                product_result = await session.execute(
                    select(Product).where(Product.name == product_name)
                )
                product = product_result.scalar_one_or_none()
                
                if product:
                    seller_product = SellerProduct(
                        seller_id=seller.id,
                        product_id=product.id,
                        active=True
                    )
                    session.add(seller_product)
            
            await session.commit()
            return True
    
    async def add_product(self, name: str, description: str = None):
        async with AsyncSessionLocal() as session:
            # Check if product already exists
            existing_result = await session.execute(
                select(Product).where(Product.name == name)
            )
            existing = existing_result.scalar_one_or_none()
            
            if existing:
                return False
            
            # Create slug from name
            slug = name.lower().replace(" ", "_").replace("-", "_")
            
            product = Product(
                name=name,
                slug=slug,
                description=description,
                active=True
            )
            session.add(product)
            await session.commit()
            return True
    
    async def give_rank(self, username: str, level: int):
        async with AsyncSessionLocal() as session:
            # Find user
            user_result = await session.execute(
                select(User).where(User.username == username)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return False
            
            # Update rank
            await session.execute(
                update(User).where(User.id == user.id).values(rank_level=level)
            )
            await session.commit()
            return True
    
    async def give_grade(self, username: str, grade: str):
        async with AsyncSessionLocal() as session:
            # Find user
            user_result = await session.execute(
                select(User).where(User.username == username)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return False
            
            # Update grade
            await session.execute(
                update(User).where(User.id == user.id).values(grade=grade)
            )
            await session.commit()
            return True
    
    async def confirm_order(self, txn_id: int):
        async with AsyncSessionLocal() as session:
            # Find transaction
            txn_result = await session.execute(
                select(Transaction).where(Transaction.id == txn_id)
            )
            transaction = txn_result.scalar_one_or_none()
            
            if not transaction or transaction.status != "pending":
                return False
            
            # Update transaction status
            await session.execute(
                update(Transaction).where(Transaction.id == txn_id).values(
                    status="confirmed",
                    confirmed_at=datetime.now()
                )
            )
            
            # Award XP to buyer
            xp_event = XPEvent(
                user_id=transaction.buyer_id,
                type="order_confirmed",
                delta=25,
                meta_json=f'{{"transaction_id": {txn_id}}}'
            )
            session.add(xp_event)
            
            # Update buyer's XP
            buyer_result = await session.execute(
                select(User).where(User.id == transaction.buyer_id)
            )
            buyer = buyer_result.scalar_one_or_none()
            
            if buyer:
                new_xp = buyer.xp_total + 25
                await session.execute(
                    update(User).where(User.id == buyer.id).values(xp_total=new_xp)
                )
            
            await session.commit()
            return True

