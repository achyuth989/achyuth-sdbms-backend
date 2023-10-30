
from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from app.model.miscellaneous import Miscellaneous

from datetime import datetime

class Service_Category(Base):
    __tablename__ = "service_category"
    service_category_id = Column(Integer, primary_key=True)
    service_category = Column(String(5), nullable=False, unique=True)
    description = Column(String(50), nullable=False)	
    service_category_indicator = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete= 'CASCADE'))
    created_by_id = Column(Integer, ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    # users = relationship("User",back_populates="Service_Category")
