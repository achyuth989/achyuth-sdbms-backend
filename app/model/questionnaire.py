from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


class Questionnaire(Base):
    __tablename__ = "questionnaire"
    questionnaire_id = Column(Integer, primary_key=True)
    question= Column(String(100), nullable=True)
    type = Column(String(30), nullable=True)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created = Column(DateTime) 
    updated_by_id = Column(Integer)
    updated = Column(DateTime)

    users = relationship("User")
