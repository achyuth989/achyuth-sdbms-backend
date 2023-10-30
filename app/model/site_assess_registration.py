from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from app.model.miscellaneous import Miscellaneous
from datetime import datetime
class Site_Assess_Registration(Base):
    __tablename__ = "site_asmt_reg_ser"
    site_asmt_reg_ser_id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))			
    experience_in_studies =  Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete="CASCADE"))
    question = Column(Integer, ForeignKey('questionnaire.questionnaire_id', ondelete='CASCADE'))
    input = Column(String(50))
    category_id = Column(Integer, ForeignKey('service_category.service_category_id', ondelete='CASCADE'))
    services = Column(String(50))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated	= Column(DateTime, onupdate=datetime.utcnow)
