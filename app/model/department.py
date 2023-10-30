from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from datetime import datetime

class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_code = Column(String(100),nullable=False,unique=True)
    department_name = Column(String(100))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated	= Column(DateTime, onupdate=datetime.utcnow)
      
