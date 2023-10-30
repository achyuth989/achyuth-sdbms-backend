from fastapi import APIRouter, Depends
from app.services.site_rec_upload_document_service import Site_Rec_Upload_documents
from app.schemas.upload_documents_schema import UploadDocuments,Details
router = APIRouter(prefix="/api")
site_rec_upload_document_service = Site_Rec_Upload_documents()

@router.get("/sitesrecognitiondetails/{site_id}")
def get_sites_rec_deatils(site_id:int):
    response  =  site_rec_upload_document_service.get_sites_rec_deatils(site_id)
    return response

@router.post("/sitesrecognitionuploaddocuments")
def add_sites_rec_upload_documents(data : UploadDocuments):
    response  =  site_rec_upload_document_service.add_sites_rec_upload_documents(data)
    return response

@router.get("/sitesrecognitionuploaddocuments/{site_id}")
def get_sites_rec_upload_documents(site_id:int):
    response  =  site_rec_upload_document_service.get_sites_rec_upload_documents(site_id)
    return response

@router.get("/uploaddocumentstatus")
def get_sites_upload_status():
    response  =  site_rec_upload_document_service.get_sites_upload_status()
    return response