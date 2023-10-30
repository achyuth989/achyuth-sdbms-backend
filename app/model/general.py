from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.miscellaneous import Miscellaneous
from sqlalchemy.dialects.postgresql import ARRAY


class General(Base):
    __tablename__ = "cr_general"
    cr_general_id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    cr_code = Column(String(100))
    salutation = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    full_name = Column(String(100))
    # last_name = Column(String(100))
    speciality = Column(Integer, ForeignKey('specialities_subspecialities.specialities_subspecialities_id', ondelete='CASCADE'))
    cr_experience= Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    certificate_of_good_clinical_practice= Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    role = Column(Integer, ForeignKey('cr_roles.cr_role_id', ondelete='CASCADE'))
    cv_available= Column(Integer, ForeignKey('miscellaneous.miscellaneous_id', ondelete='CASCADE'))
    cr_status = Column(Integer, ForeignKey('cr_status.cr_status_id'))
    clinical_phases = Column(ARRAY(String))
    reason_for_blocking = Column(String)
    created_by_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created = Column(DateTime)
    updated_by_id = Column(Integer)
    updated = Column(DateTime)




 