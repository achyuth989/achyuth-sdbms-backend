from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
#from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from sqlalchemy.dialects.postgresql import ARRAY


class Cr(Base):
    __tablename__ = "site_rec_cr"
    site_rec_cr_id = Column(Integer, primary_key=True)
    site_id  = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    cr_code= Column(String, nullable=True)
    salutation= Column(String, nullable=True)
    first_name= Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    speciality= Column(String, nullable=True)
    cr_experience= Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    certificate_of_good_clinical_practice= Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    role = Column(Integer, ForeignKey('cr_roles.cr_role_id', ondelete='CASCADE'))
    cv_available= Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    cr_status = Column(Integer, ForeignKey('cr_status.cr_status_id'))
    created_by_id= Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	=  Column(DateTime) 
    updated_by_id = Column(Integer)
    updated	=  Column(DateTime) 
    clinical_phases = Column(ARRAY(String))


    # cr_roles = relationship("Cr_Roles")
    users = relationship("User")
    sites = relationship("Site")
    # miscellaneous = relationship("Miscellaneous")
    # study_phases = relationship("StudyPhases")

