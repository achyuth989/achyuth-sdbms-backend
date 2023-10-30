from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from app.model.questionnaire import Questionnaire


class It(Base):
    __tablename__ = "site_rec_it_systems_infra"
    site_rec_it_systems_infra_id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    question = Column(Integer, ForeignKey('questionnaire.questionnaire_id', ondelete='CASCADE'))
    answer = Column(ARRAY(String))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    input = Column(String, nullable=True)                                     
    created =  Column(DateTime)
    updated_by_id = Column(Integer)
    updated	=  Column(DateTime) 


    users = relationship("User")
    sites = relationship("Site")
    # miscellaneous = relationship("Miscellaneous")
