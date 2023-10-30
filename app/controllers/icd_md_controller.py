from typing import List
from fastapi import APIRouter,Depends
from app.schemas.icd_md_schema import icd
from app.services.icd_md_services import icd_md_data


router = APIRouter(prefix="/api")
icd_data = icd_md_data()

@router.post("/icdmd")
def Add_icd_data(data:icd):
    response =  icd_data.post_icd_data(data)
    return response

@router.get("/allicdmd/{user_id}")
def Get_icdmd(user_id:int):
    response = icd_data.get_icd_data_all(user_id)
    return response

@router.get("/icdmda/{id}")
def Get_icd_all_data_icd(id:str):
    response = icd_data.get_icd_data(id)
    return response

@router.delete("/icdmda/{id}")
def delete_icd_md(id:int):
    response = icd_data.get_delete_icd(id)
    return response


# @router.get("/siteicd")
# def get_icd_level():
#     response = icd_data.get_site()
#     return response
