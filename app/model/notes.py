from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.institution import Institution

class Note(Base):
    __tablename__ = "notes"
    note_id=Column(Integer,primary_key=True)
    type = Column(String(length=30),nullable=True)
    description = Column(String,nullable=True)
    entity_id = Column(Integer)
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True) 

