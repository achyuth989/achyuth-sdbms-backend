from typing import List
from fastapi import APIRouter, Depends
from app.schemas.cr_status_schema import Cr_Status, Update_Cr_Status
from app.services.cr_status_service import Cr_Status_Service

router = APIRouter(prefix="/api")
cr_status_service = Cr_Status_Service()

@router.post("/crstatus")
def add_cr_status(data:Cr_Status):
    response = cr_status_service.add_cr_status(data)
    return response

# @router.get("/crstatus")
# def get_cr_status():
#     response = cr_status_service.get_cr_status()
#     return response 
# get data by org, taking user_id as input paramter
@router.get("/allcrstatus/{user_id}")
def get_cr_status_related_to_org(user_id:int):
    response = cr_status_service.get_cr_status(user_id)
    return response 

@router.get("/crstatus/{id}")
def cr_status(id:int):
    response = cr_status_service.cr_status(id)
    return response  

@router.put("/crstatus/{id}")
def update_cr_status(id:int,data:Update_Cr_Status):
    response = cr_status_service.update_cr_status(id,data)
    return response              