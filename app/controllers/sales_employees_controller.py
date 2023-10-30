from fastapi import APIRouter, Depends,UploadFile, HTTPException, status
from app.schemas.sales_employees_schema import SalesEmployees, UpdateSalesEmployees
from app.services.sales_employees_service import Sales_Employees_Service
import os
import pandas as pd
from sqlalchemy.orm import Session 
import logging
# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Create a logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")
sales_employees_service = Sales_Employees_Service()

@router.post("/salesemployee")
def add_sales_employee(emp_details: SalesEmployees):
    response  =  sales_employees_service.add_sales_employee(emp_details)
    return response
# @router.get("/salesemployee")
# def get_sales_employees():
#     emp_list  = sales_employees_service.sales_employees_list()
#     return emp_list
# get data by org, taking user_id as input paramter
@router.get("/allsalesemployees/{user_id}")
def get_sales_employees_related_to_org(user_id:int):
    emp_list  = sales_employees_service.sales_employees_list(user_id)
    return emp_list


@router.get("/salesemployee/{id}")
def sales_employee_details(id:int):
    emp_details = sales_employees_service.sales_employee_details(id)
    return emp_details    
@router.put("/salesemployee/{id}")
def update_employee_details(id:int , sales_emp_details: UpdateSalesEmployees):
    emp_details = sales_employees_service.update_employee_details(id, sales_emp_details)
    return emp_details
   
# def post_files_employees(self,database_url):
#         self.engine = create_engine(database_url)
#         self.Session = sessionmaker(bind=self.engine)
    
def is_valid_file(filename: str):
        return filename.endswith(('.csv', '.xlsx','.xls'))
    
    
def save_uploaded_file(file: UploadFile):
        filename = os.path.basename(file.filename)
        os.makedirs("temp", exist_ok=True)
        temp_file_path = os.path.join("temp", filename)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.file.read())        
        return temp_file_path
    
@router.post("/salesemployee/upload-file/{id}")
async def upload_file(file: UploadFile, id:int):
    if not is_valid_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # Save the uploaded file to a temporary location
    temp_file_path = save_uploaded_file(file)
    print("Temporary file path:", temp_file_path)
    response = sales_employees_service.process_uploaded_file(temp_file_path,id)
    return response
    # except Exception as e:
    #     logger.error("Error occurred during processing:", exc_info=True)
    #     print("Error:", str(e))
    #     return {"error": "Error occurred while uploading and processing the data"}
   
  

        



