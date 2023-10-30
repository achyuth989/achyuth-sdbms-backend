from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Date
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.site import Site
from app.model.miscellaneous import Miscellaneous
from app.model.study_phases import StudyPhases
from app.model.questionnaire import Questionnaire
from app.model.research_product import Research_Product


class Cr_infra(Base):
    __tablename__="site_rec_cr_infra"
    site_rec_cr_infra_id =Column(Integer,primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    question = Column(Integer, ForeignKey('questionnaire.questionnaire_id',ondelete='CASCADE'))
    answer = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    phase_study_ids = Column(String(50))
    research_product_ids = Column(String(50))
    study_name = Column(String(50))
    type_of_study = Column(String(50))
    phase_id = Column(Integer, ForeignKey('study_phases.study_phase_id', ondelete='CASCADE'))
    sponsor = Column(String(50))
    no_of_patients_recruited = Column(Integer)
    start_date = Column(Date)			
    end_date = Column(Date)	
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    
    site_obj = relationship('Site')
    # questionary_obj = relationship('Questionary')
    # miscellaneous_obj = relationship('Miscellaneous')
    users_obj = relationship("User")
    
    

