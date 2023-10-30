from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.model.state import State
from datetime import datetime
from app.model.cities import City
from app.model.user import User
from app.model.country_state_muni_trn import CountryStateMuniTrn
# from app.model.miscellaneous import Miscellaneous
class Institution(Base): 
    __tablename__ = "institutions"
    institution_id = Column(Integer, primary_key=True)
    institution_code = Column(String(length=10),unique = True,nullable=False)
    institution_name = Column(String(length=60),nullable=False)
    address_1 = Column(String(length=80),nullable=False)
    address_2 = Column(String(length=80),nullable=True)
    address_3 = Column(String(length=80),nullable=True)
    address_4 = Column(String(length=80),nullable=True)
    country_state_muni_trn_id = Column(Integer,ForeignKey('country_state_muni_trn.country_state_muni_trn_id',ondelete='CASCADE'))  
    # state = Column(Integer, ForeignKey('state.state_id',ondelete='CASCADE')) 
    # city = Column(Integer, ForeignKey('cities.city_id',ondelete='CASCADE')) 
    district = Column(String(length=40),nullable=True)
    region = Column(String(length=50),nullable=True)
    pin_code = Column(String(length=12),nullable=True)
    # country = Column(Integer, ForeignKey('geography.geography_id',ondelete='CASCADE'))
    website = Column(String(length=60), nullable=True)
    status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer, nullable=True)
    updated = Column(DateTime, onupdate=datetime.utcnow, nullable=True)    
    # country_obj = relationship('Country')
    # city_obj = relationship('City')
    user_obj = relationship('User')

    # country_obj = relationship('Geography')  
    # city = relationship('City')  