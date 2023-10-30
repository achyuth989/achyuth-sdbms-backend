from typing import List
from fastapi import APIRouter, Depends
from app.schemas.it_schema import It, ItUpdate
from app.services.it_service import It_Service

router = APIRouter(prefix="/api")
it_service = It_Service()

@router.post("/post_it_and_system_infra")
def post_it_and_system_infra(add_it: It):
    response = it_service.post_it_and_system_infra(add_it)
    return response

@router.get("/get_it_and_system_infra")
def get_all_it_and_system_infra():
    response = it_service.get_all_it_and_system_infra()
    return response


@router.put("/put_it_and_system_infra/{site_id}")
def put_it_and_system_infra(site_id: int, updated_it: ItUpdate):
    response = it_service.update_it_and_system_infra(site_id, updated_it)
    return response

@router.get("/get_it_and_system_infra_by_id/{site_id}")
def get_it_and_system_infra_by_site_id(site_id: int):
    response = it_service.get_by_site_id(site_id)
    return response

