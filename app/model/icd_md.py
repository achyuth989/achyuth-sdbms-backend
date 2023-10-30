from pydantic import BaseModel
from app.db.database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.model.user import User
from app.model.icd import Icd
from datetime import datetime


class Icd_Md(Base):

    __tablename__ = "md_icd_site"
    
    icd_id = Column(Integer,primary_key=True,autoincrement=True)
    site_id = Column(Integer,ForeignKey('sites.site_id',ondelete= 'CASCADE'))
    icd_code = Column(String)
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)

