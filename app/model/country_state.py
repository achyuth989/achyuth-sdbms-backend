from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.country_details import CountryDetails
from app.model.state import State

class CountryState(Base):
    __tablename__ = "country_state"
    country_state_id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey('country_details.country_id', ondelete = 'CASCADE'))
    state_id   = Column(Integer, ForeignKey('state.state_id', ondelete = 'CASCADE'))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'))
    created	= Column(DateTime, default= datetime.utcnow)
    updated_by_id = Column(Integer, nullable = True)
    updated	= Column(DateTime, onupdate = datetime.utcnow)
