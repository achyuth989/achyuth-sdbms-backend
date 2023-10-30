from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, BigInteger, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "sdbms_db_audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(100))
    record_id = Column(Integer)
    column_name = Column(String(100))
    old_value = Column(Text)  
    new_value = Column(Text)
    site_id = Column(Integer)
    action = Column(String(100))
    action_date = Column(DateTime, default=datetime.utcnow)
    performed_by_id = Column(String(100))


   