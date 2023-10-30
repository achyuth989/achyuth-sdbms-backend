from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User


research_product_table = Table(
    "research_products", Base.metadata,
    Column("research_product_id", Integer, primary_key=True),
    Column("product_id", String(length=10), nullable=False,unique=True),
    Column("research_product_type", String(length=40), nullable=False),
    Column("product_description",String(length=50),nullable=False),
    Column("created_by_id", Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column("created", DateTime, default=datetime.utcnow),
    Column("updated_by_id", Integer, nullable=True),
    Column("updated", DateTime, onupdate=datetime.utcnow, nullable=True)
)

class Research_Product(Base):
    __table__ = research_product_table