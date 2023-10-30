from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
 
class City(Base):
    __tablename__ = "cities"
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(30), nullable=False)
    country_id = Column(Integer, ForeignKey('geography.geography_id', ondelete="CASCADE"))  
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    # countries_obj = relationship("Geography")
