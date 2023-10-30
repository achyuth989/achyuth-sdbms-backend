from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Contacts(Base):
    __tablename__ = "contacts"
    contact_id = Column(Integer, primary_key=True, autoincrement=True)
    screen_capture = Column(String(30))
    capture_id = Column(Integer)
    contact_name = Column(String(60), nullable=True)
    role = Column(String(60),nullable=True)  
    office_telephone = Column(BigInteger,nullable=True)
    extension = Column(String(10),nullable=True)
    mobile_number = Column(BigInteger,nullable=True)
    email = Column(String(80),nullable=True)
    created_by_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)