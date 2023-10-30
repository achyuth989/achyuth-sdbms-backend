from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


class GeneralAffiliations(Base):
    __tablename__ = "cr_gen_facilities_affiliations"
    cr_gen_fac_aff_id = Column(Integer, primary_key=True)
    cr_general_id = Column(Integer, ForeignKey('cr_general.cr_general_id', ondelete='CASCADE'))   
    primary_facility = Column(String, nullable=True)
    facility_department_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created = Column(DateTime)
    updated_by_id = Column(Integer)
    updated = Column(DateTime)
