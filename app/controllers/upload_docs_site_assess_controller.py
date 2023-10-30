from typing import List
from fastapi import APIRouter,Depends
from app.services.upload_docs_site_assess_service import Upload_Docs_Site_Assess_Service
from app.schemas.upload_docs_site_assess_schema import Upload_Site_Assess_Docs, Update_Upload_Site_Assess_Docs

router = APIRouter(prefix="/api")
upload_docs_site_assess_service  = Upload_Docs_Site_Assess_Service()

@router.get("/getsiteassessdocuments/{id}")
def Get_Site_Assess_Docs(id:int):
    response = upload_docs_site_assess_service.get_site_assess_docs(id)
    return response

@router.post("/siteassessuploaddocuments")
def Post_Site_Assess_Docs(data:Upload_Site_Assess_Docs):
    response = upload_docs_site_assess_service.post_site_assess_docs(data)
    return response

@router.get("/siteassessuploaddocuments/{id}")
def Get_Uploaded_Site_Assess_Docs(id:int):
    response = upload_docs_site_assess_service.get_uploaded_site_assess_docs(id)
    return response

@router.put("/siteassessuploaddocuments")
def Update_Uploaded_Site_Assess_Docs(data:Update_Upload_Site_Assess_Docs):
    response = upload_docs_site_assess_service.update_uploaded_site_assess_docs(data)
    return response    