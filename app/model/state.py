from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
class State(Base):
    __tablename__ = "state"
    state_id = Column(Integer, primary_key=True, autoincrement=True)
    state_name   = Column(String(100))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'))
    created	= Column(DateTime, default= datetime.utcnow)
    updated_by_id = Column(Integer, nullable = True)
    updated	= Column(DateTime, onupdate = datetime.utcnow)
    state_code = Column(String)
