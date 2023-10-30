from typing import List
from fastapi import  APIRouter,Depends
from app.schemas.siteassement_orgpersonal_schema import Siteassementorg,Updatesiteassessment
from app.services.siteassement_orgpersonal_service import Siteassment_org_personal

router = APIRouter(prefix="/api")
sitteassment_org = Siteassment_org_personal()


@router.post("/siteassorg")
def Add_siteass_org(data:Siteassementorg):
    response = sitteassment_org.post_orgpersonal(data)
    return response

@router.get("/siteassorg/{site_id}")
def Add_siteass_org(site_id:int):
    response = sitteassment_org.get_orgpersonal_by_id(site_id)
    return response

@router.put("/siteassorg/{id}")
def update_siteass_org(id:int,data:Updatesiteassessment):
    response = sitteassment_org.update_orgpersonal(id,data)
    return response

@router.delete("/siteassorg/{id}")
def delete_icd_md(id:int):
    response = sitteassment_org.get_delete_orgpersonal(id)
    return response
