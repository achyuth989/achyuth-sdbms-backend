from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from datetime import datetime


class Document_Status(Base):

    __tablename__ = "document_status"

    documentstatus_id  = Column(Integer,primary_key=True,)
    document_status_id = Column(String(5),nullable=False,unique=True)
    document_status_description = Column(String(30),nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)

