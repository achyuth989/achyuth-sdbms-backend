from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


class GeneralEducation(Base):
    __tablename__ = "cr_gen_education"
    cr_gen_edu_id = Column(Integer, primary_key=True)
    cr_general_id = Column(Integer, ForeignKey('cr_general.cr_general_id', ondelete='CASCADE'))
    degree_certificate = Column(String, nullable=True)
    institution = Column(String, nullable=True)
    speciality = Column(String, nullable=True)
    year_completed = Column(Integer)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created = Column(DateTime)
    updated_by_id = Column(Integer)
    updated = Column(DateTime)
