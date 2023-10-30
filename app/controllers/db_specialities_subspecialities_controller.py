from typing import List
from fastapi import APIRouter, Depends
from app.services.db_specialities_subspecialities_service import Db_Specialities_Subspecialities_Service
from app.schemas.specialities_schema import Dbspecialities

router = APIRouter(prefix="/api")
db_specialities_subspecialities_service = Db_Specialities_Subspecialities_Service()

# get data by org, taking user_id as input paramter
@router.get("/alldbspecialities/{user_id}")
def get_all_specialities_related_to_org(user_id:int):
    response  =  db_specialities_subspecialities_service.get_all_specialities(user_id)
    return response 

@router.get("/dbspecialities/{id}")
def get_specialities(id:int):
    response  =  db_specialities_subspecialities_service.get_specialities(id)
    return response     

@router.post("/dbspecialities")
def add_specialities(data:Dbspecialities):
    response  =  db_specialities_subspecialities_service.add_specialities(data)
    return response   

@router.get("/specialitieslist/{user_id}")
def get_specialities_list(user_id:int):
    response  =  db_specialities_subspecialities_service.get_specialities_list(user_id)
    return response     