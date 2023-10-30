from fastapi import APIRouter, Depends
from app.schemas.department_schema import Department,Updatedepartment
from app.services.department_service import Department_service
router = APIRouter(prefix="/api")
department_services = Department_service()
@router.post("/department")
def  add_department(data:Department):
    response= department_services.add_department(data)
    return response
# @router.get("/department")
# def get_departments():
#     response = department_services.department_list()
#     return response
# get data by org, taking user_id as input paramter
@router.get("/departments/{user_id}")
def get_all_departments_related_to_org(user_id:int):
    response = department_services.department_list(user_id)
    return response

@router.put("/department/{id}")
def update_department(id:int,Department:Updatedepartment):
    response = department_services.update_department(id,Department)
    return response
@router.get("/department/{id}")
def get_all_departments(id:int):
    response = department_services.get_all_departments(id)
    return response


    

