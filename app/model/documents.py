from pydantic import BaseModel
from app.db.database import Base
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.model.user import User
from datetime import datetime

class Documents(Base):

    __tablename__ = "md_documents_site"

    document_id = Column(Integer, primary_key=True)
    site_id = Column(Integer,ForeignKey('sites.site_id', ondelete='CASCADE'))
    # document_code = Column(String(10),nullable=False)
    short_name = Column(String(60),nullable=False)
    document_description = Column(String(100),nullable=False)
    caterogy = Column(Integer,ForeignKey('document_category.document_category_id', ondelete='CASCADE'))
    remarks = Column(String(100),nullable=True)
    created_by_id = Column(Integer,ForeignKey('users.id', ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)    
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)