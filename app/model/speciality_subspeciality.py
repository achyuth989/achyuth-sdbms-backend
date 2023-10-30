from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.speciality import Speciality
from datetime import datetime

class SpecialitySubspeciality(Base):
    __tablename__ = 'speciality_subspeciality'
    id = Column(Integer, primary_key=True)
    speciality_id = Column(Integer, ForeignKey('speciality.id'))
    subspeciality = Column(String(100))
    # speciality = relationship("Speciality", back_populates="subspecialities")

