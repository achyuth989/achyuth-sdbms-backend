from pydantic import BaseModel
from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from app.model.site import Site
from app.model.equipment_mapping import Equipment_Mapping
from app.model.miscellaneous import Miscellaneous
from datetime import datetime

class Md_Equipments_Site(Base):
    __tablename__ = "md_equipments_site"  
    md_equipment_site_id = Column(Integer, primary_key=True,autoincrement=True)
    site_id = Column(Integer,ForeignKey('sites.site_id',ondelete= 'CASCADE'))
    equipment_mapping_id = Column(Integer,ForeignKey('equipment_mapping.equipment_mapping_id',ondelete= 'CASCADE'))
    equipment_type = Column(String(10), nullable=False)
    equipment_name = Column(String(50), nullable=False)
    status = Column(Integer,ForeignKey('miscellaneous.miscellaneous_id',ondelete= 'CASCADE'))
    created_by_id = Column(Integer, ForeignKey('users.id',ondelete= 'CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)