from pydantic import BaseModel
from app.db.database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from datetime import datetime
from app.model.user import User
from sqlalchemy.orm import relationship





class Icd(Base):

    __tablename__ = "icd"
    icd_id = Column(Integer,primary_key=True,autoincrement=True)
    icd_code = Column(String(10))
    description = Column(String(225))
    parent = Column(String(10))
    icd_level = Column(Integer)
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)

    # created_by = relationship("User", foreign_keys=[created_by_id], back_populates="created_icds")
    # updated_by = relationship("User", foreign_keys=[updated_by_id], back_populates="updated_icds")
