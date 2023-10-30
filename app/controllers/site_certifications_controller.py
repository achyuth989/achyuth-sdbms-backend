from typing import List
from fastapi import APIRouter,Depends
from app.schemas.site_certifications_schema import Site_Certificates,Updatesitecertifications
from app.services.site_certifications_services import  Site_Certificatess

router = APIRouter(prefix="/api")
site_certificate  = Site_Certificatess()

@router.post("/sitecertifications")
def Add_Site_certifications(data:Site_Certificates):
    response = site_certificate.Site_Certifications(data)
    return response


# @router.get("/sitecertifications")
# def Get_Site_certifications_all():
#     response = site_certificate.get_site_certifications_all()
#     return response
# get data by org, taking user_id as input paramter
@router.get("/allcertifications/{user_id}")
def Get_Site_certifications_related_to_org(user_id:int):
    response = site_certificate.get_site_certifications_all(user_id)
    return response

@router.get("/sitecertifications/{id}")
def sitecertifications_by_id(id:int):
      response = site_certificate.get_site_certifications_by_id(id)
      return response

@router.put("/sitecertifications/{id}")
def update_site_certifications(id:int,Site_Certifications:Updatesitecertifications):
    response = site_certificate.update_site_certifications(id,Site_Certifications)
    return response