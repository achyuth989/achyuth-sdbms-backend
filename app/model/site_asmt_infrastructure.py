from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Date,DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.site import Site
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous

class SiteAsmtInfrastructure(Base):
    __tablename__ ="site_asmt_infra_equal"
    site_asmt_infra_equal_id = Column(Integer,primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    question = Column(Integer, ForeignKey('questionnaire.questionnaire_id',ondelete='CASCADE'))
    answer = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    input = Column(String(50))
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    # created = Column(DateTime)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    
    site_obj = relationship('Site')
    # questionary_obj = relationship('Questionary')
    # miscellaneous_obj = relationship('Miscellaneous')
    users_obj = relationship("User")