from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User

class Geography(Base):
    __tablename__ = "geography"
    geography_id = Column(Integer,primary_key=True)
    country_code = Column(Integer,ForeignKey('country_details.country_id',ondelete='CASCADE'))
    country_description = Column(Integer,ForeignKey('country_details.country_id',ondelete='CASCADE'))
    region_code = Column(Integer,ForeignKey('country_details.country_id',ondelete='CASCADE'))
    region_description = Column(Integer,ForeignKey('country_details.country_id',ondelete='CASCADE'))
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)

    # users = relationship('User')