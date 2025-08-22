from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from services.database import Base

class SellerProduct(Base):
    __tablename__ = "seller_products"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(String, nullable=True) # Price can be flexible, so string
    active = Column(Boolean, default=True)

    __table_args__ = (UniqueConstraint('seller_id', 'product_id', name='_seller_product_uc'),)


