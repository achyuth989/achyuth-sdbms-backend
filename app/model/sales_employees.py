from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from app.model.department import Department

class SalesEmployees(Base):
    __tablename__ = "sales_employees"
    sales_employee_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_code = Column(String(10), unique=True, nullable=False)
    employee_name = Column(String(30), nullable=False)
    role = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=True)			
    end_date = Column(Date, nullable=True)
    department = Column(ARRAY(String))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))		 
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)	         
    updated	= Column(DateTime, onupdate=datetime.utcnow)	  
    user_obj = relationship('User')      