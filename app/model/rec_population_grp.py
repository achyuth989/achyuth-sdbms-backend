from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from sqlalchemy.dialects.postgresql import ARRAY

class Rec_Population_grp(Base):
    __tablename__ = "site_rec_pop_group"
    site_rec_pop_grp_id = Column(Integer, primary_key=True, autoincrement=True)
    site_id	= Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    pop_service_on_site_id = Column(ARRAY(String))
    specialities_subspecialities_id = Column(Integer)
    question	= Column(Integer)
    answer = Column(Integer)
    input = Column(Integer)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated	= Column(DateTime, onupdate=datetime.utcnow)
    user_obj = relationship('User')

    