from pydantic import BaseModel
from datetime import datetime,date
from typing import List
class AddSiteEquipment(BaseModel):
    site_id :int = None 
    equipment_type:int = None  
    equipment_instrument_name :int = None
    brand :str = None 
    model :str = None 
    serial_number :str = None 
    capacity_range :str = None  
    instrument_id :str = None 
    last_maintenance_date :date = None				
    next_maintenance_date :date = None	
    calibration_qualification :str = None 
    validity :date = None		
    remarks :str = None 
    equipment_id :int = None
    created_by_id : int = None


class Filterequipment(BaseModel):
    site_id: List[int] = None
    site_equipment_id:int=None
    md_equipment_site_id:int = None

    
# class AddSiteEquipment(BaseModel):
#     addsiteequipment : List[SiteEquipment] = None