from pydantic import BaseModel
from datetime import datetime


class Organizations_Schema(BaseModel):
    id: int
    org_name : str = None
    org_address : str = None
    created_by_id:int = None
    
class Org_Status_Schema(BaseModel):
    id : int
    updated_by_id : int = None
