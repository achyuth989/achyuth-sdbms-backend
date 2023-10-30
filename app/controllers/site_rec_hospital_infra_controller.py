from fastapi import APIRouter, Depends
from app.schemas.site_rec_hospital_infra_schema import hospitalinfra,questions,services,updatehospitalinfra
from app.services.site_rec_hospital_infra_service import Site_Rec_Hospital_Infra
router = APIRouter(prefix="/api")
site_rec_hospital_infra_service = Site_Rec_Hospital_Infra()
@router.post("/hospitalinfra")
def post_sites_rec_hospital_infra(hospital_infra : hospitalinfra):
    response  =  site_rec_hospital_infra_service.post_sites_rec_hospital_infra(hospital_infra)
    return response
@router.get("/hospitalinfra/{site_id}")
def get_sites_rec_hospital_infra(site_id : int):
    response  =  site_rec_hospital_infra_service.get_sites_rec_hospital_infra(site_id)
    return response
@router.get("/hospitalinfraservices/{site_id}/{category_id}")
def get_sites_rec_hospital_infra_services(site_id : int, category_id: int):
    response  =  site_rec_hospital_infra_service.get_sites_rec_hospital_infra_services(site_id,category_id)
    return response
@router.put("/hospitalinfra/{site_id}")
def update_sites_rec_hospital_infra(site_id : int, update_hospital_infra : updatehospitalinfra):
    response  =  site_rec_hospital_infra_service.update_sites_rec_hospital_infra(site_id,update_hospital_infra)
    return response