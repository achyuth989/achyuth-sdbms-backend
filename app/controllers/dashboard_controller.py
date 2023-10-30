from fastapi import APIRouter, Depends
from app.services.dashboard_service import Dashboard

router = APIRouter(prefix="/api")
dashboard_service = Dashboard()

@router.get("/dashboard/{user_id}")
async def get_dashboard_related_to_org(user_id:int):
    response = dashboard_service.get_dashboard_data(user_id)
    return response

@router.get("/dashboard-map/{user_id}")
async def get_dashboard_map_data_related_to_org(user_id:int):
    response = dashboard_service.get_dashboard_map_data(user_id)
    return response

@router.get("/dashboard-icd/{user_id}")
async def get_dashboard_icd_data_related_to_org(user_id:int):
    response = dashboard_service.get_dashboard_icd_data(user_id)
    return response