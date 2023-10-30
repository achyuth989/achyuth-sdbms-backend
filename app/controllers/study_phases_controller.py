from fastapi import APIRouter, Depends
from app.schemas.study_phases_schema import StudyPhases,Updatestudyphases
from app.services.study_phases_service import Study_Phases_Service
router = APIRouter(prefix="/api")
study_phases_service = Study_Phases_Service()
@router.post("/studyphases")
def add_study_phases(study_phases_details : StudyPhases ):
    response = study_phases_service.add_study_phases(study_phases_details)
    return response
# @router.get("/studyphases")
# def get_study_phases():
#     response = study_phases_service.study_phases_list()
#     return response
# get data by org, taking user_id as input paramter
@router.get("/allstudyphases/{user_id}")
def get_study_phases_related_to_org(user_id:int):
    response = study_phases_service.study_phases_list(user_id)
    return response

@router.put("/studyphases/{id}")
def update_study_phase(id:int,StudyPhases:Updatestudyphases):
    response = study_phases_service.update_study_phases(id,StudyPhases)
    return response

@router.get("/studyphases/{id}")
def get_study_phase(id:int):
    response = study_phases_service.get_study_phase(id)
    return response    
