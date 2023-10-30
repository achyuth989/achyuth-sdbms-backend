from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User

population_group_served_table = Table(
    "population_group_served", Base.metadata,
    Column("population_group_served_id", Integer, primary_key=True),
    Column("population_group_id", String(length=30), nullable=False, unique=True),
    Column("population_group_description", String(length=70), nullable=False),
    Column("created_by_id", Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column("created", DateTime, default=datetime.utcnow),
    Column("updated_by_id", Integer),
    Column("updated", DateTime, onupdate=datetime.utcnow, nullable=True)
)

class Population_Group(Base):
    __table__ = population_group_served_table
