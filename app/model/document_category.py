from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from datetime import datetime
class DocumentCategory(Base):
    __tablename__ = "document_category"
    document_category_id = Column(Integer, primary_key=True, autoincrement=True)
    document_category = Column(String(15), nullable=False,unique=True)			
    description = Column(String(50), nullable=False)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated	= Column(DateTime, onupdate=datetime.utcnow)
    user_obj = relationship('User')