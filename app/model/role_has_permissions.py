from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, Date,ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.role_master import Role_Master
from app.model.permissions import Permissions
class Role_Has_Permissions(Base):
    __tablename__ = "role_has_permissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id	= Column(Integer, ForeignKey('role_master.role_master_id', ondelete='CASCADE'))	
    permissions_id = Column(Integer, ForeignKey('permissions.id', ondelete='CASCADE'))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    updated_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created	= Column(DateTime, default=datetime.utcnow)
    updated	= Column(DateTime, onupdate=datetime.utcnow)