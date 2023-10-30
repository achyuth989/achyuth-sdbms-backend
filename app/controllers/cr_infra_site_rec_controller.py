from typing import List
from fastapi import APIRouter, Depends
from app.services.cr_infra_site_rec_service import Cr_Infra_Service
from app.schemas.cr_infra_site_rec import Cr_infra,Questionary_List,Research_List

router = APIRouter(prefix="/api")
cr_infra_service = Cr_Infra_Service()

@router.post("/cr-infra")
def add_and_update_cr_infra_new_details(cr_infra:Cr_infra):
    response = cr_infra_service.add_cr_infra_details(cr_infra)
    return response

# @router.get("/cr-infra")
# def get_all_sites_cr_infra_details():
#     response = cr_infra_service.get_cr_infra_details()
#     return response

@router.get("/cr-infra/{site_id}")
def get_cr_infra_by_site_id(site_id:int):
    response = cr_infra_service.get_cr_infra_details_by_site_id(site_id)
    return response

@router.delete("/cr-infra/{site_id}/{site_rec_cr_infra_id}")
def delete_cr_infra_by_site_id_and_cr_infra_id(site_id:int,site_rec_cr_infra_id:int):
    response = cr_infra_service.delete_cr_infra_details_by_site_id_and_cr_infra_id(site_id,site_rec_cr_infra_id)
    return response




# @router.put("/cr_infra/{site_id}")
# def put_cr_infra(site_id: int, Cr_infra_edit: Cr_infra_edit):
#     response = cr_infra_service.edit_cr_infra(site_id, Cr_infra_edit)
#     return response
