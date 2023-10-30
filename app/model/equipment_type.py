from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User

equipment_type_table = Table(
    "equipment_type", Base.metadata,
    Column("equipment_type_id", Integer, primary_key=True),
    Column("equipment_code", String(length=10), nullable=False,unique=True),
    Column("equipment_type", String(length=10), nullable=False),
    Column("equipment_description", String(length=50), nullable=False),
    Column("created_by_id", Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column("created", DateTime, default=datetime.utcnow),
    Column("updated_by_id", Integer),
    Column("updated", DateTime, onupdate=datetime.utcnow, nullable=True)
)

class Equipment_Type(Base):
    __table__ = equipment_type_table