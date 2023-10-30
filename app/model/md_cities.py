from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
 
class Md_Cities(Base):
    __tablename__ = "md_cities"
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(String(10)) 
    city =Column(String(80))  

    # countries_obj = relationship("Geography")
