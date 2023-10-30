from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Organizations(Base):
    __tablename__ = "organizations"
    id = Column(Integer,primary_key=True)
    org_name = Column(String(length=100), nullable=True)
    org_address = Column(String(200))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True) 
    status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id'))      
    # created_by = relationship('User', foreign_keys=[created_by_id])    