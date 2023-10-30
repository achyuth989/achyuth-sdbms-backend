from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Address(Base):
    __tablename__ = "site_address"
    site_address_id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer,ForeignKey('sites.site_id',ondelete='CASCADE'))
    as_per_license = Column(String(5), nullable=True)
    address_1 = Column(String(80),nullable=True)  
    address_2 = Column(String(80),nullable=True)
    address_3 = Column(String(80),nullable=True)
    address_4 = Column(String(80),nullable=True)
    city = Column(Integer,nullable=True)
    district = Column(String(40))
    region = Column(String(40))
    pincode = Column(String(40))
    country = Column(Integer,nullable=True)
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)