from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table, Date
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime
from app.model.user import User
from app.model.site import Site
from app.model.miscellaneous import Miscellaneous
from app.model.cr import Cr
from app.model.institution import Institution
from app.model.license_type import LicenseType
from app.model.country_details import CountryDetails
from app.model.specialities_subspecialities import SpecialitySubspeciality
from app.model.speciality import Speciality
from app.model.icd import Icd


# from app.model.study_phases import StudyPhases
# from app.model.questionnaire import Questionnaire
# from app.model.research_product import Research_Product


# parent table
class Cr_Research_Exp_Check_List(Base):
    __tablename__= "cr_research_exp_check_list"
    cr_res_exp_check_list_id = Column(Integer, primary_key=True)
    # site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    cr_general_id = Column(Integer, ForeignKey('cr_general.cr_general_id',ondelete='CASCADE'))
    study_type = Column(String(20))
    clinical_study_phases = Column(String(20))
    speciality_cie10 = Column(String(20))
    cv = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    scanned_id = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    scanned_title = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    scanned_license = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    IATA_training = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    # attachment = Column(String(70))
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)


class Cr_Professional_Experience(Base):
    __tablename__ = "cr_professional_experience"
    cr_prof_exp_id = Column(Integer, primary_key=True)
    cr_general_id = Column(Integer, ForeignKey('cr_general.cr_general_id',ondelete='CASCADE'))
    # site_id = Column(Integer, ForeignKey('sites.site_id', ondelete='CASCADE'))
    # cr_res_exp_check_list_id = Column(Integer, ForeignKey('cr_research_exp_check_list.cr_res_exp_check_list_id', ondelete='CASCADE'))
    job_title = Column(String(35))
    institution_department = Column(String(50))
    year_started = Column(Date)	
    year_completed = Column(Date)	
    # attachment = Column(String(70))
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    
class Cr_License_Ense(Base):
    __tablename__ = "cr_license_ense"
    cr_lic_ense_id = Column(Integer, primary_key=True)
    cr_general_id = Column(Integer, ForeignKey('cr_general.cr_general_id',ondelete='CASCADE'))
    # cr_res_exp_check_list_id = Column(Integer, ForeignKey('cr_research_exp_check_list.cr_res_exp_check_list_id', ondelete='CASCADE'))
    type_of_license = Column(Integer, ForeignKey('license_type.license_type_id', ondelete='CASCADE'))
    license_issuer = Column(String(30))
    professional_license_number = Column(String(30))
    state_region = Column(Integer, ForeignKey('country_details.country_id', ondelete='CASCADE'))
    country = Column(Integer, ForeignKey('country_details.country_id', ondelete='CASCADE'))
    issue_date = Column(Date)
    expiration_date = Column(Date)
    # attachment = Column(String(70))
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    
class Cr_Gcp_Trai(Base):
    __tablename__ = "cr_gcp_trai"
    cr_res_exp_id = Column(Integer, primary_key=True)
    cr_general_id = Column(Integer, ForeignKey('cr_general.cr_general_id',ondelete='CASCADE'))
    # cr_res_exp_check_list_id = Column(Integer, ForeignKey('cr_research_exp_check_list.cr_res_exp_check_list_id', ondelete='CASCADE'))
    training_provider = Column(String(30))
    title_of_training = Column(String(30))
    version = Column(String(10))
    date_completed = Column(Date)
    status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    # attachment = Column(String(70))
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    

    
class Cr_Specialities(Base):
    __tablename__ = "cr_specialities"
    cr_theura_area_exp_id = Column(Integer, primary_key=True)
    cr_general_id = Column(Integer, ForeignKey('cr_general.cr_general_id',ondelete='CASCADE'))
    # cr_res_exp_check_list_id = Column(Integer, ForeignKey('cr_research_exp_check_list.cr_res_exp_check_list_id', ondelete='CASCADE'))
    specialities = Column(Integer, ForeignKey('speciality.id',ondelete='CASCADE'))
    sub_specialities = Column(Integer, ForeignKey('speciality_subspeciality.id',ondelete='CASCADE'))
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    
class Cr_Total_Clinical_Research_Exp(Base):
    __tablename__ = "cr_total_clinical_research_exp"
    cr_tot_cli_res_exp_id = Column(Integer, primary_key=True)
    cr_general_id = Column(Integer, ForeignKey('cr_general.cr_general_id',ondelete='CASCADE'))
    # cr_res_exp_check_list_id = Column(Integer, ForeignKey('cr_research_exp_check_list.cr_res_exp_check_list_id', ondelete='CASCADE'))
    total_therapeutic_area = Column(Integer,ForeignKey('icd.icd_id'))
    total_sub_therapeutic_area = Column(Integer,ForeignKey('icd.icd_id'))
    sponsor_name = Column(String(70))
    cro_name = Column(String(70))
    no_of_completed_studies = Column(Integer)
    no_of_ongoing_studies = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Integer, ForeignKey('miscellaneous.miscellaneous_id',ondelete='CASCADE'))
    # attachment = Column(String(70))
    created_by_id = Column(Integer,ForeignKey('users.id'))
    created = Column(DateTime, default=datetime.utcnow)
    updated_by_id = Column(Integer)
    updated = Column(DateTime, onupdate=datetime.utcnow)
    


    
    
    
    
    
    