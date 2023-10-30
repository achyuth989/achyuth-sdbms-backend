from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from datetime import datetime


class Study_Type(Base):

    __tablename__ = "study_types"

    studytype_id = Column(Integer,primary_key=True)
    study_type_id = Column(String(10),nullable=False,unique=True)
    study_type	= Column(String(20),nullable=False)
    description = Column(String(50),nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow) 
 