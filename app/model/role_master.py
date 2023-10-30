from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
# from app.model.user import User
from app.model.miscellaneous import Miscellaneous
from datetime import datetime


class Role_Master(Base):
    __tablename__ = "role_master"
    
    role_master_id  =Column(Integer, primary_key=True)
    role = Column(String(100), nullable=False, unique=True)
    role_description =Column(String(100))
    status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    created_by_id = Column(Integer, ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)