from typing import List
from fastapi import APIRouter, Depends
from app.schemas.cr_schema import Cr, CrUpdate, Cr_Schema, Cr_Schema_Update
from app.services.cr_service import Cr_Service

router = APIRouter(prefix="/api")
cr_service = Cr_Service()

@router.post("/post_cr")
def post_clinical_researchers(add_cr: Cr_Schema):
    response = cr_service.post_cr(add_cr)
    return response

@router.get("/get_cr")
def get_clinical_researchers():
    response = cr_service.get_cr()
    return response


@router.put("/put_clinical_researchers/{site_id}")
def put_clinical_researchers(site_id: int, update_cr_list: Cr_Schema_Update):
    response = cr_service.update_cr(site_id, update_cr_list)
    return response


@router.get("/get_cr/{site_id}")
def get_clinical_researchers_by_id(site_id:int):
    response = cr_service.get_cr_by_id(site_id)
    return response

@router.delete("/get_cr/{id}")
def delete_clinical_researcher(id:int):
    response = cr_service.delete_cr(id)
    return response