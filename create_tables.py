from app.db.database import Base,engine
from app.model.user import User
from app.model.country_details import CountryDetails
from app.model.geography import Geography
from app.model.cities import City
from app.model.miscellaneous import Miscellaneous
from app.model.institution import Institution
from app.model.department import Department
from app.model.sales_employees import SalesEmployees
from app.model.site import Site
from app.model.notes import Note
from app.model.site_rec_hospital_infra import SiteRecHospitalInfra
from app.model.population_group import Population_Group
from app.model.equipment_type import Equipment_Type
from app.model.research_product import Research_Product
from app.model.cr_status import Cr_Status
from app.model.document_status import Document_Status
from app.model.study_type import Study_Type
# from app.model.site_services import SiteServices
from app.model.site_certifications import Site_Certifications
from app.model.service_category import Service_Category
from app.model.cr_roles import  Cr_Roles
from app.model.services import Site_Services
from app.model.document_category import DocumentCategory
from app.model.study_phases import StudyPhases
from app.model.license_type import LicenseType
from app.model.site import Site
from app.model.icd import Icd
# from app.model.specialities import Specialities
from app.model.icd_md import Icd_Md
from app.model.documents import Documents
from app.model.address import Address
from app.model.cr_infra_site_rec import Cr_infra
from app.model.md_cities import Md_Cities
from app.model.contacts import Contacts
from app.model.cr import Cr
from app.model.it import It
from app.model.icd_siterecgonization import Siteicd
from app.model.site_rec_hr import Siterec_hr
from app.model.regulatory_info_site_rec import RegulatoryInfo
from app.model.rec_population_grp import Rec_Population_grp
from app.model.siteassement_orgpersonal import Orgpersonal
from app.model.site_assess_registration import Site_Assess_Registration
from app.model.equipment_mapping import Equipment_Mapping
from app.model.md_equipments_site import Md_Equipments_Site
from app.model.site_asmt_infrastructure import SiteAsmtInfrastructure
# from app.model.specialities_subspecialities import Specalitiess
from app.model.site_equipment import Site_Equipment
from app.model.site_services import SiteServices
from app.model.cr_professional_experience import Cr_Research_Exp_Check_List,Cr_Professional_Experience,Cr_License_Ense,Cr_Gcp_Trai,Cr_Specialities,Cr_Total_Clinical_Research_Exp
from app.model.site_assess_review import Site_Assess_Review
from app.model.legal import Legal
from app.model.upload_documents import Upload_Documents
from app.model.quality_systems import QualitySystems
from app.model.cr_gen_education import GeneralEducation
from app.model.cr_gen_education import GeneralEducation
from app.model.cr_gen_facilities_affiliations import GeneralAffiliations
from app.model.general import General
from app.model.audit_log import AuditLog
from app.model.department import Department
from app.model.state import State
from app.model.country_state import CountryState
from app.model.country_state_muni import CountryStateMuni
from app.model.country_state_muni_trn import CountryStateMuniTrn
from app.model.role_master import Role_Master
from app.model.permissions import Permissions
from app.model.role_has_permissions import Role_Has_Permissions
from app.model.organizations import Organizations
from app.model.contact_role import ContactRole

Base.metadata.create_all(engine)
