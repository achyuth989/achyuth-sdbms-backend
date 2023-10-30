
from pydantic import BaseModel
from app.db.database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.model.user import User
from datetime import datetime


class Cr_Roles(Base):

    __tablename__ = "cr_roles"

    cr_role_id = Column(Integer, primary_key=True)
    cr_id = Column(String(10),nullable=False,unique=True)
    cr_role = Column(String(30),nullable=False)
    description = Column(String(50),nullable=False)
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
