from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.role_master import Role_Master

# from app.model.institution import Institution
from app.model.miscellaneous import Miscellaneous
from app.model.organizations import Organizations

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	email = Column(String, nullable=True)
	password = Column(String, nullable=True)
	role_id = Column(Integer, ForeignKey('role_master.role_master_id'))
	name = Column(String, nullable=True)
	status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id'))
	created_by_id = Column(Integer, ForeignKey('users.id'))
	created = Column(DateTime, default=datetime.utcnow)
	updated_by_id = Column(Integer, nullable=True)
	updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
	org_id = Column(Integer, ForeignKey('organizations.id'))
	
	# site_rec_it_systems_infra = relationship("It")
	# site_rec_cr = relationship("Cr")
	# site_rec_it_systems_infra = relationship("It")
	# site_rec_cr = relationship("Cr")
	# site_rec_questionary = relationship("Questionary")


