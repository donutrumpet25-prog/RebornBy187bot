from sqlalchemy import Column, Integer, String
from services.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sector_number = Column(Integer, nullable=False)
    slug = Column(String, unique=True, nullable=False)


