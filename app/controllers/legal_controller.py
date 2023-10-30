from typing import List
from fastapi import APIRouter, Depends
from app.schemas.legal_schema import Legal, LegalUpdate
from app.services.legal_service import Legal_Service

router = APIRouter(prefix="/api")
legal_service = Legal_Service()

@router.post("/post_it_and_legal_docs")
def post_legal_docs(add_legal: Legal):
    response = legal_service.post_legal_docs(add_legal)
    return response

@router.get("/get_legal_docs")
def get_all_legal_docs():
    response = legal_service.get_all_legal_docs()
    return response


@router.put("/put_legal_docs/{site_id}")
def put_legal_docs(site_id: int, updated_legal: LegalUpdate):
    response = legal_service.update_legal_docs(site_id, updated_legal)
    return response

@router.get("/get_legal_docs_by_site_id/{site_id}")
def get_legal_docs_by_site_id(site_id: int):
    response = legal_service.get_by_site_id(site_id)
    return response