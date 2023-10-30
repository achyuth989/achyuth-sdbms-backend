from typing import List
from fastapi import APIRouter, Depends
from app.schemas.equipment_type_schema import Equipment_Type, Update_Equipment_Type
from app.services.equipment_type_service import Equipment_Type_Service

router = APIRouter(prefix="/api")
equipment_type_service = Equipment_Type_Service()

@router.post("/equipmenttype")
def add_equipment_type(data:Equipment_Type):
    response = equipment_type_service.add_equipment_type(data)
    return response

@router.get("/equipmenttype")
def get_equipment_type():
    response = equipment_type_service.get_equipment_types()
    return response    

@router.get("/equipmenttype/{id}")
def equipment_type(id:int):
    response = equipment_type_service.equipment_type(id)
    return response

@router.put("/equipmenttype/{id}")
def update_equipment_type(id:int,data:Update_Equipment_Type):
    response = equipment_type_service.update_equipment_type(id,data)
    return response        