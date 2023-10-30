from typing import List
from fastapi import APIRouter,Depends
from app.schemas.upload_doc_cr_schema import Cr_Doc_Upload,Edit_Cr_Doc_Upload, Versions
from app.services.upload_doc_cr_service import Upload_Doc_cr_Service


router = APIRouter(prefix="/api")
upload_doc_cr_service  = Upload_Doc_cr_Service()

@router.get("/cr-docs/{cr_id}")
def get_cr_docs(cr_id:int):
    response = upload_doc_cr_service.get_cr_doc_details(cr_id)
    return response

@router.post("/cr-docs")
def get_cr_docs(data : Cr_Doc_Upload):
    response = upload_doc_cr_service.post_cr_doc_details(data)
    return response

@router.get("/cr-docs-view/{cr_id}")
def get_cr_docs(cr_id:int):
    response = upload_doc_cr_service.get_cr_doc_View(cr_id)
    return response

@router.put("/cr-docs")
def add_and_update_cr_docs(data : Edit_Cr_Doc_Upload):
    response = upload_doc_cr_service.put_cr_doc_details(data)
    return response

@router.get("/get-uploaded-document/{document_id}")
def get_uploaded_document(document_id:int):
    response = upload_doc_cr_service.get_uploaded_document(document_id)
    return response    
