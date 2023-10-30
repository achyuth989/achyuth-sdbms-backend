from typing import List
from fastapi import APIRouter,Depends
from app.schemas.specialities_schema import Specialitiessubspecialities,Updatespecialities
from app.services.icd_service import Icd_Service
from app.services.specialities_services import SpecilaitiesSubspecialities

router = APIRouter(prefix="/api")
special  = SpecilaitiesSubspecialities()

@router.post("/specialities")
def Add_specialities(data:Specialitiessubspecialities):
    response = special.get_specialities(data)
    return response

@router.get("/specialities")
def Get_specialities_all():
    response = special.get_specialities_all()
    return response


@router.get("/specialities/{id}")
def Specialities_by_id(id:int):
    response = special.get_specialities_id(id)
    return response

@router.put("/specialities/{id}")
def Specialities_by_id(id:int,Specialities:Updatespecialities):
    response = special.put_spcialities(id,Specialities)
    return response