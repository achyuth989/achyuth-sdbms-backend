from typing import List
from fastapi import APIRouter, Depends
from app.schemas.equipment_mapping_schema import Equipment_Mapping, Update_Equipment_Mapping
from app.services.equipment_mapping_service import Equipment_Mapping_Service

router = APIRouter(prefix="/api")
equipment_mapping_service = Equipment_Mapping_Service()

@router.post("/equipmentmapping")
def add_equipment_mapping(data:Equipment_Mapping):
    response = equipment_mapping_service.add_equipment_mapping(data)
    return response

# @router.get("/equipmentmapping")
# def get_equipment_mapping():
#     response = equipment_mapping_service.get_equipment_mapping()
#     return response   
# get data by org, taking user_id as input paramter
@router.get("/allequipmentmapping/{user_id}")
def get_equipment_mapping_related_to_org(user_id:int):
    response = equipment_mapping_service.get_equipment_mapping(user_id)
    return response   

@router.get("/equipmentmapping/{id}")
def equipment_mapping(id:int):
    response = equipment_mapping_service.equipment_mapping(id)
    return response

@router.put("/equipmentmapping/{id}")
def update_equipment_mapping(id:int,data:Update_Equipment_Mapping):
    response = equipment_mapping_service.update_equipment_mapping(id,data)
    return response        

@router.get("/equipmentnames/{id}")
def get_equipment_names(id:int):
    response = equipment_mapping_service.get_equipment_names(id)
    return response