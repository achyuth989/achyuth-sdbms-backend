from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.site import Site
from app.model.miscellaneous import Miscellaneous
from app.model.document_status import Document_Status
from app.model.cr import Cr
class Upload_Documents(Base):
    __tablename__ = "upload_documents"
    upload_document_id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete = 'CASCADE'))
    cr_code = Column(Integer, ForeignKey('site_rec_cr.site_rec_cr_id', ondelete = 'CASCADE'))
    screen_type_name = Column(String(30))
    screen_label_name = Column(String(100))
    document_name = Column(String(300))
    document_attached = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete = 'CASCADE'))
    version = Column(String(20))
    status = Column(Integer, ForeignKey('document_status.documentstatus_id', ondelete = 'CASCADE'))
    remarks = Column(String(100))
    attachment = Column(String(100))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'))
    created = Column(DateTime, default= datetime.utcnow)
    updated_by_id = Column(Integer, nullable = True)
    updated = Column(DateTime, onupdate = datetime.utcnow)
