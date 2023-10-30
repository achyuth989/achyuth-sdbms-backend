from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from app.model.site import Site
from app.model.service_category import Service_Category
from datetime import datetime

class Site_Services(Base):
    
    __tablename__ = "md_services_site"
    
    service_id = Column(Integer, primary_key=True,autoincrement=True)
    site_id = Column(Integer,ForeignKey('sites.site_id',ondelete= 'CASCADE'))
    service_category = Column(Integer,ForeignKey('service_category.service_category_id',ondelete= 'CASCADE'))
    services = Column(Integer,ForeignKey('site_services.site_ser_id',ondelete= 'CASCADE'))
    # short_name = Column(String(60), nullable=False)
    remarks = Column(String(100), nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    # users = relationship("User",back_populates="services")

