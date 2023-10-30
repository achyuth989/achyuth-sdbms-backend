from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.site import Site
from app.model.icd import Icd
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from app.model.user import User
from datetime import datetime


class Siteicd(Base):

    __tablename__ = "site_rec_icd"

    site_rec_icd_id = Column(Integer,primary_key = True)
    site_id = Column(Integer,ForeignKey('sites.site_id', ondelete='CASCADE'))
    top_icd_id = Column(Integer,ForeignKey('icd.icd_id', ondelete='CASCADE'))
    top_diseases_pathologies = Column(String(50))
    top_count_of_thread = Column(String(30))
    question = Column(Integer,ForeignKey('questionnaire.questionnaire_id',ondelete='CASCADE'))
    answer = Column(Integer,ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    orphan_icd_id = Column(Integer,ForeignKey('icd.icd_id', ondelete='CASCADE'))
    orphan_diseases_pathologies = Column(String(50))
    orphan_count_of_thread = Column(String(30))
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)


    # icds = relationship("Icd", back_populates="siteicd", foreign_keys="[Icd.site_id]")


