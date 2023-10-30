from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from app.model.site import Site
from app.model.md_equipments_site import Md_Equipments_Site
from datetime import datetime,date
class Site_Equipment(Base):
    __tablename__ = "site_equipment"
    site_equipment_id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    md_equipment_site_id = Column(Integer, ForeignKey('md_equipments_site.md_equipment_site_id', ondelete='CASCADE'))
    equipment_type = Column(String(10), nullable=False)
    equipment_instrument_name = Column(String(50), nullable=False)
    brand = Column(String(30))
    model = Column(String(20))
    serial_number = Column(String(30))
    capacity_range = Column(String(25))
    # site_location = Column(String(30))
    instrument_id = Column(String(10))
    last_maintenance_date = Column(Date, nullable=True, default=None)			
    next_maintenance_date = Column(Date, nullable=True, default=None)	
    calibration_qualification = Column(String(20))
    validity = 	Column(Date, nullable=True, default=None)	
    remarks = Column(String(50))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))		 
    created	= Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)	         
    updated	= Column(DateTime, onupdate=datetime.utcnow)