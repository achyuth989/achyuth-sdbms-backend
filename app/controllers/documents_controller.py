from typing import List
from fastapi import APIRouter, Depends
from app.schemas.documents_schema import Documents, Update_Documents, AdditionalDocuments
from app.services.documents_service import Documents_Service

router = APIRouter(prefix="/api")
documents_service = Documents_Service()

@router.post("/documents")
def add_documents(data:Documents):
    response = documents_service.add_documents(data)
    return response

@router.get("/alldocuments/{user_id}")
def get_documents(user_id:int):
    response = documents_service.get_documents(user_id)
    return response 

@router.get("/documents/{id}")
def documents(id:int):
    response = documents_service.documents(id)
    return response  

@router.put("/documents/{id}")
def update_documents(id:int,data:Update_Documents):
    response = documents_service.update_documents(id,data)
    return response              