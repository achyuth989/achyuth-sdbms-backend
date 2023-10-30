
from typing import List
from fastapi import APIRouter,Depends
from app.schemas.cr_roles_schema import Crroles, Updatecrroles
from app.services.cr_roles_service import  Cr_Roless


router = APIRouter(prefix="/api")
cr_roles = Cr_Roless()

@router.post("/crroles")
def Add_Cr_Roles(data:Crroles):
    response = cr_roles.Cr_Roles(data)
    return response


# @router.get("/crroles")
# def Get_Cr_Roles_all():
#     response = cr_roles.get_cr_roles()
#     return response

# get data by org, taking user_id as input paramter
@router.get("/allcrroles/{user_id}")
def Get_Cr_Roles_all_related_to_org(user_id:int):
    response = cr_roles.get_cr_roles(user_id)
    return response

@router.get("/crroles/{id}")
def Cr_roles_by_id(id:int):
      response = cr_roles.get_cr_roles_by_id(id)
      return response

@router.put("/crroles/{id}")
def update_cr_roles(id:int , Cr_Roles:Updatecrroles):
    crroles_details = cr_roles.Update_cr_roles(id,Cr_Roles)
    return crroles_details
