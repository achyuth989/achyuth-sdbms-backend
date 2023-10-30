from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Date
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.site import Site
from app.model.miscellaneous import Miscellaneous
from app.model.document_category import DocumentCategory

class RegulatoryInfo(Base):
    __tablename__="site_rec_regulatory_information"
    site_rec_reg_info_id= Column(Integer,primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    document_category_id = Column(Integer, ForeignKey('document_category.document_category_id', ondelete='CASCADE'))
    document = Column(String(50))
    availability = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    date = Column(Date)
    remarks = Column(String(30))
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    
    site_obj = relationship('Site')
    # questionary_obj = relationship('Questionary')
    # miscellaneous_obj = relationship('Miscellaneous')
    users_obj = relationship("User")
    