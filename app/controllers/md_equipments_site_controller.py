from typing import List
from fastapi import APIRouter, Depends
from app.schemas.md_equipments_site_schema import Equipment,UpdateEquipmentStatus
from app.services.md_equipments_site_service import Md_Equipments_Site_Service

router = APIRouter(prefix="/api")
md_equipments_site_service = Md_Equipments_Site_Service()

@router.post("/equipment")
def add_equipment(data:Equipment):
    response = md_equipments_site_service.add_equipment(data)
    return response

@router.get("/allequipment/{user_id}")
def get_equipment(user_id:int):
    response = md_equipments_site_service.get_equipment(user_id)
    return response    

@router.get("/equipment/{id}")
def get_equipment_by_id(id:int):
    response = md_equipments_site_service.get_equipment_by_id(id)
    return response

@router.put("/equipment/{id}")
def status_equipment(id:int,data : UpdateEquipmentStatus):
    response = md_equipments_site_service.status_equipment(id,data)
    return response 

@router.get("/equipments/{site_id}")
def get_equipment_by_site_id(site_id:int):
    response = md_equipments_site_service.get_equipment_by_site_id(site_id)
    return response

@router.get("/uniqueequipmenttype/{site_id}")
def get_equipment_by_site_id_distinct(site_id:int):
    response = md_equipments_site_service.get_equipment_by_site_id_distinct(site_id)
    return response

@router.get("/equipmentnames/{site_id}/{id}")
def get_equipment_names_by_site_id(site_id:int, id:int):
    response = md_equipments_site_service.get_equipment_names_by_site_id(site_id,id)
    return response

@router.get("/sitequipmenttypebyequipment/{equipmentype_id}")
def filter_site_equipment(equipmentype_id:int):
    response = md_equipments_site_service.get_equipment_type_names(equipmentype_id)
    return response
