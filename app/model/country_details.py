from pydantic import BaseModel
from app.db.database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.model.user import User
from datetime import datetime

class CountryDetails(Base):
    __tablename__ = "country_details"
    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String(30))
    country_code = Column(String(10))
    region = Column(String(30))
    region_code = Column(String(10))