from typing import List
from fastapi import  APIRouter,Depends
from app.schemas.services_schema import Services,Updateservices
from app.services.service_service import Service

router = APIRouter(prefix="/api")
services = Service()

@router.post("/services")
def service(data:Services):
      response  = services.add_service(data)
      return response

@router.get("/services")
def service_all():
    response = services.get_site_service_all()
    return response

@router.get("/services/{id}")
def service_by_id(id:int):
      response = services.get_site_service_by_id(id)
      return response
      
@router.put("/services/{id}")
def update_services(id:int,Site_Services:Updateservices):
      response = services.update_site_service_by_id(id,Site_Services)
      return response