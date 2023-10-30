from pydantic import BaseModel
from datetime import datetime,date
from typing import List

class SalesEmployees(BaseModel):
    employee_code :str = None		 
    employee_name :str = None			 
    role :str = None			 
    start_date :date = None		
    end_date :date	= None
    department:List[str]	
    created_by_id :int = None	

class UpdateSalesEmployees(BaseModel):         
    employee_name :str = None             
    role :str = None             
    start_date :date = None        
    end_date :date    = None   
    department:List[str]	
    updated_by_id :int = None
        	 
class Config:
    orm_mode = True