from typing import List
from fastapi import APIRouter, Depends
from app.services.organizations_service import Organizations_Service
from app.schemas.organizations_schema import Organizations_Schema, Org_Status_Schema

router = APIRouter(prefix="/api")
organizations_service = Organizations_Service()

@router.post("/organizations")
async def add_and_update_organizations(data:Organizations_Schema):
    response = organizations_service.add_update_organizations(data)
    return response

@router.get("/all-organizations")
def get_all_organizations():
    response = organizations_service.get_all_org_details()
    return response

@router.get("/organizations/{org_id}")
def get_organization_by_id(org_id:int):
    response = organizations_service.get_org_details_by_org_id(org_id)
    return response

@router.put("/update-organization-status")
def update_organzation_status(data:Org_Status_Schema):
    response = organizations_service.update_org_status_by_id(data)
    return response

@router.get("/active-organizations")
def get_active_organizations():
    response = organizations_service.get_all_active_organizations()
    return response
