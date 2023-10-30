from pydantic import BaseModel
from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.model.site_services import SiteServices
from app.model.user import User



class Site_Certifications(Base):

    __tablename__ = "site_certifications"

    site_certification_id = Column(Integer,primary_key=True)
    certification_id = Column(String(10),nullable=False,unique=True)
    service_category_description = Column(Integer,ForeignKey('site_services.site_ser_id',ondelete= 'CASCADE'))
    certification_description   = Column(String(60),nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete= 'CASCADE'))
    created  = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated  = Column(DateTime, onupdate=datetime.utcnow)