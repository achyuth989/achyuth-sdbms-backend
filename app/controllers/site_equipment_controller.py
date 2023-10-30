from fastapi import APIRouter, Depends
from app.schemas.site_equipment_schema import AddSiteEquipment,Filterequipment
from app.services.site_equipment_service import Site_Equipments
router = APIRouter(prefix="/api")
site_equipment_service = Site_Equipments()
@router.post("/siteequipment")
def site_equipment(siteequipmentdetails : AddSiteEquipment):
    response  =  site_equipment_service.post_site_equipment(siteequipmentdetails)
    return response
@router.get("/siteequipment/{site_id}")
def get_site_equipment(site_id:int):
    response  =  site_equipment_service.get_site_equipment(site_id)
    return response

@router.get("/searchsitestatus")
def search_sites_status(site_id:int=None , site_status:int = None):
    response  =  site_equipment_service.search_sites_status(site_id,site_status)
    return response  

@router.get("/site_equipment_status")
def get_site_equipment_stauts():
    response = site_equipment_service.get_site_equip_status()
    return response

@router.post("/filtersitequipment")
def filter_site_equipment(data:Filterequipment):
    response = site_equipment_service.filter_site_equipment(data)
    return response 

@router.get("/site_equipment_all/{user_id}")
def get_site_equipment_stauts(user_id:int):
    response = site_equipment_service.get_site_equipment_all(user_id)
    return response
# @router.post("sitequipmenttypebyequipment")
# def filter_site_equipment(data:Filterequipment):
#     response = site_equipment_service.get_equipment_type_names(data)
#     return response
