from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.questionnaire import Questionnaire


class Legal(Base):
    __tablename__ = "site_asmt_doc"
    site_asmt_doc_id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    question = Column(Integer, ForeignKey('questionnaire.questionnaire_id', ondelete='CASCADE'))
    answer = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created = Column(DateTime)
    updated_by_id = Column(Integer)
    updated = Column(DateTime) 

    users = relationship("User")
    sites = relationship("Site")
    miscellaneous = relationship("Miscellaneous")
