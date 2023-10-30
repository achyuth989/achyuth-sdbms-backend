from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, Date,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
class Permissions(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, autoincrement=True)		
    permission_name = Column(String(30))
    screen_type = Column(String(50))
    screen_name = Column(String(50))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    updated_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated	= Column(DateTime, onupdate=datetime.utcnow)