from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
class LicenseType(Base):
    __tablename__ = "license_type"
    license_type_id = Column(Integer, primary_key=True, autoincrement=True)
    license_id	= Column(String(10), nullable=False,unique=True)
    license_type = Column(String(20), nullable=False)
    description	= Column(String(50), nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated	= Column(DateTime, onupdate=datetime.utcnow)
    user_obj = relationship('User')