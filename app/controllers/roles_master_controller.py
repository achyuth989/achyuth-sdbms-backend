from typing import List
from fastapi import APIRouter,Depends
from app.schemas.role_master_schema import Role_master, UpdateRolemaster, StatusChange
from app.services.role_master_service import  Role_masters
from app.services.role_master_service import  Permissions_Service
router = APIRouter(prefix="/api")
roles_master = Role_masters()
permissions_service = Permissions_Service()

@router.post("/rolesmaster")
def Add_Role_Masters(data:Role_master):
    response = roles_master.Role_Master_Services(data)
    return response


@router.get("/rolesmaster/{org_id}")
def Get_All_Role_Masters(org_id:int):
    response = roles_master.get_all_role_masters(org_id)
    return response

@router.get("/activerolesmaster/{org_id}")
def Get_All_Active_Role_Masters(org_id:int):
    response = roles_master.get_all_active_role_masters(org_id)
    return response

@router.get("/rolesmaster")
def Get_All_Role_Masters_data():
    response = roles_master.get_all_role_masters_data()
    return response

# @router.get("/rolemaster/{id}/{org_id}")
# def Roles_Master_Id(id:int, org_id: int):
#       response = roles_master.roles_master_id(id,org_id)
#       return response

@router.put("/rolesmaster/{id}")
def update_roles_masters(id:int , Role_masters:UpdateRolemaster):
    roles_details = roles_master.update_roles_masters(id,Role_masters)
    return roles_details

@router.get("/permissions")
def permissions_list():
      response = permissions_service.permissions_list()
      return response

@router.put("/rolesmasterstatus/{role_id}")
def change_roles_status(role_id:int , data : StatusChange):
    roles_details = roles_master.change_roles_status(role_id,data)
    return roles_details