import asyncio
from services.profile_service import ProfileService
from services.marketplace_service import MarketplaceService
from services.referral_service import ReferralService
from services.admin_service import AdminService
from services.ranking_service import RankingService
from services.clasament_service import ClasamentService

async def comprehensive_test():
    print("🧪 Running comprehensive functionality test...")
    
    try:
        # Test 1: Create a test user
        profile_service = ProfileService()
        user = await profile_service.create_or_update_user(123456789, "testuser", "Test User")
        print(f"✅ Test 1: User created - ID: {user.id}")
        
        # Test 2: Test marketplace
        marketplace_service = MarketplaceService()
        products = await marketplace_service.get_all_products()
        locations = await marketplace_service.get_all_locations()
        print(f"✅ Test 2: Marketplace - {len(products)} products, {len(locations)} locations")
        
        # Test 3: Test admin functions
        admin_service = AdminService()
        seller_added = await admin_service.add_seller("testuser")
        print(f"✅ Test 3: Admin - Seller added: {seller_added}")
        
        # Test 4: Test referral system
        referral_service = ReferralService()
        referral_code = await referral_service.get_or_create_referral_code(123456789)
        print(f"✅ Test 4: Referral - Code generated: {referral_code}")
        
        # Test 5: Test ranking system
        ranking_service = RankingService()
        progress = await ranking_service.get_user_progress(123456789)
        print(f"✅ Test 5: Ranking - User progress: {progress}")
        
        # Test 6: Test leaderboard
        clasament_service = ClasamentService()
        leaderboard = await clasament_service.get_leaderboard("all", 1)
        print(f"✅ Test 6: Leaderboard - {len(leaderboard)} entries")
        
        print("🎉 All comprehensive tests passed!")
        
    except Exception as e:
        print(f"❌ Comprehensive test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(comprehensive_test())
