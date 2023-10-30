from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.questionnaire import Questionnaire
from app.model.site import Site
from app.model.miscellaneous import Miscellaneous
from app.model.site_rec_hr import Siterec_hr
from app.model.user import User
from datetime import datetime



class Orgpersonal(Base):
    __tablename__ = "site_asmt_org_pers"

    site_asmt_org_pers_id = Column(Integer,primary_key=True)
    site_id = Column(Integer,ForeignKey('sites.site_id', ondelete='CASCADE'))
    role = Column(String)
    salutation = Column(String(30))
    first_name = Column(String(30))
    last_name = Column(String(30))
    contact_phone =Column(BigInteger)
    contact_email = Column(String)
    question = Column(Integer,ForeignKey('questionnaire.questionnaire_id',ondelete='CASCADE'))
    input = Column(String(50))
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
