from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User

cr_status_table = Table(
    "cr_status", Base.metadata,
    Column("cr_status_id", Integer, primary_key=True),
    Column("cr_id", String(length=10), nullable=False,unique=True),
    Column("cr_status", String(length=20), nullable=False),
    Column("description", String(length=100)),
    Column("created_by_id", Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column("created", DateTime, default=datetime.utcnow),
    Column("updated_by_id", Integer),
    Column("updated", DateTime, onupdate=datetime.utcnow, nullable=True)
)

class Cr_Status(Base):
    __table__ = cr_status_table
