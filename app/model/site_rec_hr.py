from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.questionnaire import Questionnaire
from app.model.cr_roles import Cr_Roles
from app.model.site import Site
from app.model.user import User
from app.model.specialities_subspecialities import Specalitiess
from datetime import datetime

class Siterec_hr(Base):


    __tablename__ = "site_rec_hr"

    site_rec_hr_id = Column(Integer,primary_key=True)
    site_id = Column(Integer,ForeignKey('sites.site_id', ondelete='CASCADE'))
    question = Column(Integer,ForeignKey('questionnaire.questionnaire_id',ondelete='CASCADE'))
    answer = Column(Integer,ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    input= Column(Integer)
    speciality_subspeciality_id = Column(Integer,ForeignKey('specialities_subspecialities.specialities_subspecialities_id'))
    count = Column(Integer)
    role = Column(String(30))
    salutation = Column(Integer,ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    first_name = Column(String(30))
    last_name = Column(String(30))
    stand = Column(String(30))
    contact_phone = Column(Integer)
    contact_email = Column(String)
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)