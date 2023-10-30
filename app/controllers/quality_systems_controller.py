from typing import List
from fastapi import APIRouter, Depends
from app.schemas.quality_systems_schema import QualitySystems, QualitySystemsUpdate
from app.services.quality_systems_service import QualitySystems_Service

router = APIRouter(prefix="/api")
qualitysystems_service = QualitySystems_Service()

@router.post("/post_quality_systems")
def post_quality_systems(add_qualitysystems: QualitySystems):
    response = qualitysystems_service.post_qualitysystems(add_qualitysystems)
    return response

@router.get("/get_quality_systems")
def get_quality_systems():
    response = qualitysystems_service.get_qualitysystems()
    return response


@router.put("/put_quality_systems/{site_id}")
def put_quality_systems(site_id: int, updated_qualitysystems: QualitySystemsUpdate):
    response = qualitysystems_service.update_qualitysystems(site_id, updated_qualitysystems)
    return response

@router.get("/get_quality_systems_by_site_id/{site_id}")
def get_quality_systems_by_site_id(site_id: int):
    response = qualitysystems_service.get_by_site_id(site_id)
    return response

