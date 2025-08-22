from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from services.database import AsyncSessionLocal
from models.product_model import Product
from models.location_model import Location

async def initialize_products():
    """Initialize products with the specified nomenclator"""
    products = [
        {"name": "Bob Marley", "slug": "bob_marley", "description": "Premium quality product"},
        {"name": "Maroc", "slug": "maroc", "description": "High grade product"},
        {"name": "Need For Speed", "slug": "need_for_speed", "description": "Fast acting product"},
        {"name": "Power Horse", "slug": "power_horse", "description": "Strong and reliable"},
        {"name": "SnowMan", "slug": "snowman", "description": "Cool and refreshing"},
        {"name": "Breaking Bag", "slug": "breaking_bag", "description": "Available in multiple variants"},
        {"name": "2M", "slug": "2m", "description": "Breaking Bag variant"},
        {"name": "3M", "slug": "3m", "description": "Breaking Bag variant"},
        {"name": "4M", "slug": "4m", "description": "Breaking Bag variant"},
        {"name": "Berlin Calling", "slug": "berlin_calling", "description": "Premium European quality"},
        {"name": "Alice in Wonderland", "slug": "alice_in_wonderland", "description": "Magical experience"},
        {"name": "Albert Hoffman", "slug": "albert_hoffman", "description": "Research grade quality"},
        {"name": "Big Pharma", "slug": "big_pharma", "description": "Pharmaceutical grade"}
    ]
    
    async with AsyncSessionLocal() as session:
        for product_data in products:
            # Check if product already exists
            existing = await session.execute(
                select(Product).where(Product.slug == product_data["slug"])
            )
            if not existing.scalar_one_or_none():
                product = Product(**product_data, active=True)
                session.add(product)
        
        await session.commit()

async def initialize_locations():
    """Initialize locations for Bucharest sectors"""
    locations = [
        {"name": "Sector 1", "sector_number": 1, "slug": "sector_1"},
        {"name": "Sector 2", "sector_number": 2, "slug": "sector_2"},
        {"name": "Sector 3", "sector_number": 3, "slug": "sector_3"},
        {"name": "Sector 4", "sector_number": 4, "slug": "sector_4"},
        {"name": "Sector 5", "sector_number": 5, "slug": "sector_5"},
        {"name": "Sector 6", "sector_number": 6, "slug": "sector_6"}
    ]
    
    async with AsyncSessionLocal() as session:
        for location_data in locations:
            # Check if location already exists
            existing = await session.execute(
                select(Location).where(Location.slug == location_data["slug"])
            )
            if not existing.scalar_one_or_none():
                location = Location(**location_data)
                session.add(location)
        
        await session.commit()

async def initialize_all_data():
    """Initialize all required data"""
    await initialize_products()
    await initialize_locations()
    print("✅ All initial data has been created successfully!")

