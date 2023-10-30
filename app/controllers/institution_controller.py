from typing import List
from fastapi import APIRouter, Depends
from app.schemas.institution_schema import Institution, Update_Institution, Institution_Status
from app.services.institution_service import Institution_Service

router = APIRouter(prefix="/api")
institution_service = Institution_Service()

@router.post("/institution")
def add_institution(data: Institution):
    response  =  institution_service.add_institution(data)
    return response

@router.get("/allinstitution/{user_id}")
def get_institution_details(user_id:int):
    response  =  institution_service.get_institution_details(user_id)
    return response 

@router.get("/institution/{id}")
def institution_details(id:int):
    response  =  institution_service.institution_details(id)
    return response 

@router.put("/institution/{id}")
def update_institution_details(id:int,data:Update_Institution):
    response  =  institution_service.update_institution_details(id,data)
    return response            

@router.get("/geographycountries")  
def get_geographycountries():
    response  =  institution_service.get_geographycountries()
    return response  
@router.get("/geographycities/{id}")
def get_cities(id:int):
    response = institution_service.get_cities(id)
    return response

@router.delete("/deletecontact/{id}")
def delete_contact(id:int):
    response = institution_service.delete_contact(id)
    return response    

@router.put("/institutionstatus/{institution_id}")
def update_institution_status(site_id:int, data:Institution_Status):
    response  =  institution_service.update_institution_status(site_id,data)
    return response 

@router.get("/activeinstitutions")
def get_active_institution_details():
    response  =  institution_service.get_active_institution_details()
    return response          