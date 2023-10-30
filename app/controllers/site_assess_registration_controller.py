from typing import List
from fastapi import APIRouter,Depends
from app.schemas.site_assess_registration_schema import Site_Assess_Registration,Questions,Update_Site_Assess_Registration,Services
from app.services.site_assess_registration_service import  Site_Assess_Registration_Service

router = APIRouter(prefix="/api")
site_assess_registration_service  = Site_Assess_Registration_Service()

@router.post("/siteassessregistration")
def add_site_assess_registration(data : Site_Assess_Registration):
    response = site_assess_registration_service.add_site_assess_registration(data)
    return response


@router.get("/siteassessregistration/{id}")
def get_site_assess_registration(id:int):
    response = site_assess_registration_service.get_site_assess_registration(id)
    return response     

@router.put("/siteassessregistration/{id}")
def update_site_assess_registration(id:int,data:Update_Site_Assess_Registration):
    response = site_assess_registration_service.update_site_assess_registration(id,data)
    return response     