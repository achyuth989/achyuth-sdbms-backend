from typing import List
from app.schemas.icd_siterecognization_schema import Icdsite
from fastapi import APIRouter,Depends
from app.schemas.icd_siterecognization_schema import Icdsite,icds,Updateicdsite
from app.services.icd_siterecognization_service import Site_icd_diseases


router = APIRouter(prefix="/api")
icd_site = Site_icd_diseases()


@router.get("/siterecicd")
def get_icd_level():
    response = icd_site.get_site()
    return response


@router.post("/siterecicd")
def Add_site_icd(addicd:Icdsite):
    response = icd_site.post_site_icd(addicd)
    return response

@router.get("/siterecicds")
def Get_site_icd():
    response = icd_site.get_site_icd_rec()
    return response

@router.get("/siterecicds/{side_id}")
def Get_icd_siteid(side_id:int):
    response = icd_site.get_site_icd_by_siteid(side_id)
    return response

@router.put("/siterecicds/{site_id}")
def update_siteass_org(site_id:int,data:Updateicdsite):
    response = icd_site.update_icd(site_id,data)
    return response

@router.delete("/siterecicds/{id}")
def delete_icd_md(id:int):
    response = icd_site.get_delete_icd(id)
    return response