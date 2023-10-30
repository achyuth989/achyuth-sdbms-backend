from pydantic import BaseModel
from app.db.database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.model.icd import Icd
from app.model.user import User
from datetime import datetime




class Specialities(Base):

    __tablename__ = "specialities_subspecialitiess"
    specialities_subspecialities_id = Column(Integer,primary_key=True,autoincrement=True)
    icd_code = Column(Integer,ForeignKey('icd.icd_id',ondelete= 'CASCADE'))
    therapeutic_area = Column(Integer,ForeignKey('icd.icd_id',ondelete= 'CASCADE'))
    sub_therapeutic_area = Column(Integer,ForeignKey('icd.icd_id',ondelete= 'CASCADE'))
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)


