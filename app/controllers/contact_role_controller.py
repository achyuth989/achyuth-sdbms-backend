
from typing import List
from fastapi import APIRouter,Depends
from app.schemas.contact_role_schema import ContactRole, UpdateContactRole
from app.services.contact_role_service import  Contact_Role


router = APIRouter(prefix="/api")
contact_role = Contact_Role()

@router.post("/contactroles")
def Add_Contact_Roles(data:ContactRole):
    response = contact_role.add_contact_roles(data)
    return response


@router.get("/contactroles/{user_id}")
def Get_Contact_Roles(user_id:int):
    response = contact_role.get_contact_roles(user_id)
    return response

@router.put("/contactroles/{id}")
def Update_Contact_Roles(id:int , data:UpdateContactRole):
    response = contact_role.update_contact_roles(id,data)
    return response
