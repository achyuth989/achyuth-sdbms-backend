from pydantic import BaseModel
from datetime import datetime

class Research_Product(BaseModel):
    product_id:str=None
    research_product_type:str=None
    product_description:str=None
    created_by_id:int=None

class Update_Research_Product(BaseModel):
    research_product_type:str=None
    product_description:str=None
    updated_by_id:int=None    

class Config:
    orm_mode=True    