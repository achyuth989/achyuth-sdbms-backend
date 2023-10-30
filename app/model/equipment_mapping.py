from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from app.model.equipment_type import Equipment_Type
from datetime import datetime
class Equipment_Mapping(Base):
    __tablename__ = "equipment_mapping"
    equipment_mapping_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_type_id = Column(Integer, ForeignKey('equipment_type.equipment_type_id', ondelete='CASCADE'))			
    equipment_name = Column(String(50), nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated	= Column(DateTime, onupdate=datetime.utcnow)
    user_obj = relationship('User')