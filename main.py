from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.user_controller import router as user_router
from app.controllers.institution_controller import router as institution_router

from app.controllers.geography_controller import router as geography_router
from app.controllers.population_group_controller import router as population_group_router
from app.controllers.equipment_type_controller import router as equipment_type_router
from app.controllers.equipment_mapping_controller import router as equipment_mapping_router
from app.controllers.research_product_controller import router as research_product_router
from app.controllers.cr_status_controller import router as cr_status_router
from app.controllers.sales_employees_controller import router as sales_employees_router
from app.controllers.document_category_controller import router as document_category_router
from app.controllers.site_services_controller import router as site_services_router
from app.controllers.study_phases_controller import router as study_phases_router
from app.controllers.license_type_controller import router as license_type_router
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.controllers.service_category_controller import router as service_category_router
from app.controllers.document_status_controller import router as document_status_router
from app.controllers.study_type_controller import router as study_type_router
from app.controllers.site_certifications_controller import router as site_certifications_router
from app.controllers.cr_roles_controller import router as cr_roles_router
from app.controllers.site_controller import router as site_router
from app.controllers.service_controller import router as service_router
from app.controllers.specialities_controller import router as specialities_router
from app.controllers.icd_controller import router as icd_router
from app.controllers.icd_md_controller import router as icd_md_router
from app.controllers.documents_controller import router as documents_router
from app.controllers.countries_controller import router as countries_router
from app.controllers.address_controller import router as address_router
from app.controllers.site_equipment_controller import router as site_equipment_router

from app.controllers.cr_controller import router as cr_router
from app.controllers.it_controller import router as it_router
from app.controllers.quality_systems_controller import router as quality_systems_router

from app.controllers.icd_siterecognization_controller import router as icd_site_router
from app.controllers.siterec_hr_controller import router as siterechr_router
from app.controllers.siteassesment_orgpersonal_controller import router as orgpersonal_router

from app.controllers.md_equipments_site_controller import router as md_equipments_site_router

from app.controllers.site_recognition_controller import router as site_rec_router
from app.controllers.regulatory_info_site_rec_controller import router as regulatory_router
from app.controllers.rec_population_grp_controller import router as rec_population_grp_router
from app.controllers.general_controller import router as general_router
from app.controllers.upload_doc_cr_controller import router as upload_doc_cr_router



from app.controllers.site_rec_hospital_infra_controller import router as site_rec_hospital_infra_router
from app.controllers.cr_infra_site_rec_controller import router as cr_infra_router
from app.controllers.regulatory_info_site_rec_controller import router as reg_info_router
from app.controllers.db_specialities_subspecialities_controller import router as db_specialities_subspecialities_router
from app.controllers.site_assess_registration_controller import router as site_assess_registration_router
from app.controllers.site_asmt_infrastructure_controller import router as site_asmt_infra_router
from app.controllers.legal_controller import router as legal_router
from app.controllers.cr_professional_experience_controller import router as cr_exp_router
from app.controllers.site_assess_review_controller import router as site_assess_review_router
from app.controllers.upload_docs_site_assess_controller import router as upload_docs_site_assess_router

from app.controllers.site_rec_upload_document_controller import router as site_rec_upload_document_router
from app.controllers.audit_log_controller import router as audit_log_router
from app.controllers.department_controller import router as department_router
from app.controllers.roles_master_controller import router as roles_master_router
from app.controllers.organizations_controller import router as org_router
from app.controllers.dashboard_controller import router as dashboard_router
from app.controllers.contact_role_controller import router as contact_role_router



app = FastAPI()

app.include_router(user_router)
app.include_router(institution_router)

app.include_router(geography_router)
app.include_router(population_group_router)
app.include_router(equipment_type_router)
app.include_router(equipment_mapping_router)
app.include_router(research_product_router)
app.include_router(cr_status_router)

app.include_router(service_category_router)
app.include_router(document_status_router)
app.include_router(study_type_router)
app.include_router(site_certifications_router)
app.include_router(cr_roles_router)
app.include_router(service_router)
app.include_router(specialities_router)
app.include_router(icd_router)
app.include_router(icd_md_router)
app.include_router(icd_site_router)
app.include_router(siterechr_router)
app.include_router(orgpersonal_router)
app.include_router(upload_doc_cr_router)



app.include_router(sales_employees_router)
app.include_router(document_category_router)
app.include_router(study_phases_router)
app.include_router(license_type_router)
app.include_router(site_services_router)
app.include_router(site_router)
app.include_router(documents_router)
app.include_router(countries_router)
app.include_router(cr_infra_router)
app.include_router(reg_info_router)

app.include_router(it_router)
app.include_router(cr_router)
app.include_router(quality_systems_router)
app.include_router(legal_router)
app.include_router(general_router)


app.include_router(address_router)
app.include_router(cr_infra_router)
app.include_router(site_rec_router)
app.include_router(regulatory_router)
app.include_router(rec_population_grp_router)

app.include_router(site_rec_hospital_infra_router)
app.include_router(db_specialities_subspecialities_router)
app.include_router(site_assess_registration_router)
app.include_router(site_assess_review_router)
app.include_router(site_asmt_infra_router)
app.include_router(md_equipments_site_router)
app.include_router(site_equipment_router)
app.include_router(upload_docs_site_assess_router)

app.include_router(site_rec_upload_document_router)
app.include_router(cr_exp_router)
app.include_router(audit_log_router)
app.include_router(department_router)
app.include_router(roles_master_router)

app.include_router(org_router)
app.include_router(dashboard_router)
app.include_router(contact_role_router)



# origins = [
#     "https://3.6.86.197:81/",
#     "http://3.6.86.197:81/",
#     "http://localhost",
#     "http://localhost:4201",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get('/')
async def home():
	return "Application Running..."
