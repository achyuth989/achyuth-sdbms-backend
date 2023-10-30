from pydantic import BaseModel
from sqlalchemy import Column, String, Integer,BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.user import User
from app.model.cities import City
from app.model.institution import Institution
from app.model.sales_employees import SalesEmployees
from app.model.miscellaneous import Miscellaneous
from app.model.country_state_muni_trn import CountryStateMuniTrn
# from app.model.it import It
from datetime import datetime

class Site(Base):
    __tablename__ = "sites"
    site_id = Column(Integer, primary_key=True, autoincrement=True)
    site_code = Column(String(10), nullable=False, unique=True)
    site_name = Column(String(100), nullable=False)
    institution_id = Column(Integer, ForeignKey('institutions.institution_id', ondelete="CASCADE"))
    address_1 = Column(String(80), nullable=False)
    address_2 = Column(String(80), nullable=True)
    address_3 = Column(String(80), nullable=True)
    address_4 = Column(String(80), nullable=True)
    # city = Column(Integer, ForeignKey('cities.city_id', ondelete="CASCADE"))
    district = Column(String(40), nullable=True)
    region = Column(String(40), nullable=True)
    pin_code = Column(String(12), nullable=True)
    country_state_muni_trn_id = Column(Integer,ForeignKey('country_state_muni_trn.country_state_muni_trn_id',ondelete='CASCADE'))  
    # country = Column(Integer, ForeignKey('geography.geography_id', ondelete="CASCADE"))
    website = Column(String(60), nullable=True)
    # responsible_sales_representative = Column(Integer, ForeignKey('sales_employees.sales_employee_id', ondelete="CASCADE"))
    status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete="CASCADE"))
    site_rec_status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete="CASCADE"))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)

    institutions_obj = relationship('Institution')
    # city_obj = relationship('City')
    # country_obj = relationship('Geography')
    # sales_emp_obj = relationship('SalesEmployees')
    users_obj = relationship("User")
    # site_rec_it_systems_infra = relationship("It")
    # site_rec_cr = relationship("Cr")
    # site_rec_questionary = relationship("Questionary")

