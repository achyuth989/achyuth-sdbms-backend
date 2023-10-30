from typing import List
from fastapi import APIRouter,Depends
from app.schemas.study_type_schema import StudyType,Updatestudytypes
from app.services.study_type_service import study_typess


router = APIRouter(prefix="/api")
study_type  = study_typess()

@router.post("/studytype")
def Add_Study_Type(data:StudyType):
    response = study_type.Study_Type(data)
    return response


# @router.get("/studytype")
# def Get_Study_Type_all():
#     response = study_type.get_study_type_all()
#     return response

# get data by org, taking user_id as input paramter

@router.get("/allstudytypes/{user_id}")
def Get_Study_Types_related_to_org(user_id:int):
    response = study_type.get_study_type_all(user_id)
    return response

@router.get("/studytype/{id}")
def Study_Type_by_id(id:int):
      response = study_type.get_study_type_by_id(id)
      return response

@router.put("/studytype/{id}")
def update_study_type(id:int,Study_Type:Updatestudytypes):
    response = study_type.update_study_type(id,Study_Type)
    return response

    
