from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from datetime import datetime

class Site_Assess_Review(Base):
    __tablename__ = "site_asmt_reviewer"
    site_asmt_reviewer_id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    date = Column(Date, nullable=True)			
    salutation = Column(String(30))
    first_name = Column(String(30))
    last_name = Column(String(30))
    role = Column(String(30))
    contact_phone = Column(BigInteger)
    review_type = Column(String(50))
    contact_email = Column(String(30))
    evaluation_mode = Column(String(20))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated	= Column(DateTime, onupdate=datetime.utcnow)
