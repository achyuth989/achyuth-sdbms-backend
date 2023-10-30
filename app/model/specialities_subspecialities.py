from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.speciality_subspeciality import SpecialitySubspeciality

class Specalitiess(Base):
    __tablename__ = "specialities_subspecialities"
    specialities_subspecialities_id = Column(Integer,primary_key=True)
    spec_sub_id = Column(Integer,ForeignKey('speciality_subspeciality.id'))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete= 'CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated	= Column(DateTime, onupdate=datetime.utcnow)