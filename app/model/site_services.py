from pydantic import BaseModel
from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.model.service_category import Service_Category
from app.model.user import User
from sqlalchemy.orm import relationship
class SiteServices(Base):
    __tablename__ = "site_services"
    site_ser_id = Column(Integer, primary_key=True, autoincrement=True)
    site_service_id = Column(String(15), nullable=False,unique=True)
    service_category = Column(Integer, ForeignKey('service_category.service_category_id', ondelete= 'CASCADE'))
    service_category_description = Column(String(60), nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete= 'CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated	= Column(DateTime, onupdate=datetime.utcnow)
    user_obj = relationship('User')
    service_obj = relationship('Service_Category')