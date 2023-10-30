from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Speciality(Base):
    __tablename__ = 'speciality'
    id = Column(Integer, primary_key=True)
    speciality = Column(String(70))
    # subspecialities = relationship("SpecialitySubspeciality", back_populates="speciality")
