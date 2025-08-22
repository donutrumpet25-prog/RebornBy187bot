from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from services.database import AsyncSessionLocal
from models.location_model import Location
from models.product_model import Product
from models.seller_model import Seller
from models.seller_product_model import SellerProduct
from models.user_model import User

class MarketplaceService:
    async def get_all_locations(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Location).order_by(Location.sector_number)
            )
            return result.scalars().all()
    
    async def get_location_by_id(self, location_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Location).where(Location.id == location_id)
            )
            return result.scalar_one_or_none()
    
    async def get_all_products(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Product).where(Product.active == True).order_by(Product.name)
            )
            return result.scalars().all()
    
    async def get_product_by_id(self, product_id: int):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            )
            return result.scalar_one_or_none()
    
    async def get_sellers_by_location(self, location_id: int, page: int = 1, per_page: int = 10):
        async with AsyncSessionLocal() as session:
            offset = (page - 1) * per_page
            result = await session.execute(
                select(Seller)
                .options(joinedload(Seller.user))
                .where(
                    Seller.location_id == location_id,
                    Seller.is_active == True
                )
                .offset(offset)
                .limit(per_page)
            )
            return result.scalars().all()
    
    async def get_sellers_by_product(self, product_id: int, page: int = 1, per_page: int = 10):
        async with AsyncSessionLocal() as session:
            offset = (page - 1) * per_page
            result = await session.execute(
                select(Seller)
                .options(joinedload(Seller.user))
                .join(SellerProduct)
                .where(
                    SellerProduct.product_id == product_id,
                    SellerProduct.active == True,
                    Seller.is_active == True
                )
                .offset(offset)
                .limit(per_page)
            )
            return result.scalars().all()
    
    async def get_all_sellers(self, page: int = 1, per_page: int = 10):
        async with AsyncSessionLocal() as session:
            offset = (page - 1) * per_page
            result = await session.execute(
                select(Seller)
                .options(joinedload(Seller.user), joinedload(Seller.location))
                .where(Seller.is_active == True)
                .offset(offset)
                .limit(per_page)
            )
            return result.scalars().all()
    
    async def get_sellers_by_sector(self, sector_number: int, page: int = 1, per_page: int = 10):
        async with AsyncSessionLocal() as session:
            offset = (page - 1) * per_page
            result = await session.execute(
                select(Seller)
                .options(joinedload(Seller.user), joinedload(Seller.location))
                .join(Location)
                .where(
                    Location.sector_number == sector_number,
                    Seller.is_active == True
                )
                .offset(offset)
                .limit(per_page)
            )
            return result.scalars().all()
    
    async def search_sellers(self, sector: int = None, product_id: int = None, min_reputation: int = None, page: int = 1, per_page: int = 10):
        async with AsyncSessionLocal() as session:
            offset = (page - 1) * per_page
            query = select(Seller).options(joinedload(Seller.user), joinedload(Seller.location))
            
            conditions = [Seller.is_active == True]
            
            if sector:
                query = query.join(Location)
                conditions.append(Location.sector_number == sector)
            
            if product_id:
                query = query.join(SellerProduct)
                conditions.append(SellerProduct.product_id == product_id)
                conditions.append(SellerProduct.active == True)
            
            if min_reputation:
                conditions.append(Seller.reputation >= min_reputation)
            
            query = query.where(*conditions).offset(offset).limit(per_page)
            
            result = await session.execute(query)
            return result.scalars().all()

