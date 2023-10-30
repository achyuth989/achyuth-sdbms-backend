from pydantic import BaseModel
from datetime import datetime
class SiteServices(BaseModel):
    site_service_id :str = None
    service_category :int = None
    service_category_description :str = None
    created_by_id :int = None

class UpdateSiteServices(BaseModel):
    service_category :int = None
    service_category_description :str = None
    updated_by_id :int = None
    
    
class Config:
    orm_mode = True