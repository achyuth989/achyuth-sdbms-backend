from pydantic import BaseModel
from sqlalchemy import Column, String,Integer,BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.site import Site
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from app.model.services import Site_Services
from app.model.user import User
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
class SiteRecHospitalInfra(Base):
    __tablename__ = "site_rec_hospital_infra"
    site_rec_hospital_infra_id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete="CASCADE"))
    question = Column(Integer, ForeignKey('questionnaire.questionnaire_id', ondelete="CASCADE"))
    answer = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete="CASCADE"))
    input = Column(String(50))
    service_category_id = Column(Integer,ForeignKey('service_category.service_category_id', ondelete="CASCADE"))
    services = Column(ARRAY(String))
    certification_of_central_laboratory_ids = Column(ARRAY(String))
    equipment_available_ids = Column(ARRAY(String))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)