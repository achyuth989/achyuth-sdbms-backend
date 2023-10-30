from typing import List
from fastapi import  APIRouter,Depends
from app.schemas.document_status_schema import DocumentStatus,Updatedocumentstatus
from app.services.document_status_service import Document_Statuss



router = APIRouter(prefix="/api")
document_status  = Document_Statuss()



@router.post("/documentstatus")
def Add_Document_Status(data:DocumentStatus):
    response = document_status.Document_Status(data)
    return response

# @router.get("/documentstatus")
# def Get_Documentstatus_all():
#     response = document_status.get_document_status_all()
#     return response
# get data by org, taking user_id as input paramter
@router.get("/alldocumentstatus/{user_id}")
def Get_all_Documentstatus_related_to_org(user_id:int):
    response = document_status.get_document_status_all(user_id)
    return response


@router.get("/documentstatus/{id}")
def Documentstatus_by_id(id:int):
      response = document_status.get_document_status_by_id(id)
      return response

@router.put("/documentstatus/{id}")
def update_document_status(id:int, Document_Status:Updatedocumentstatus):
    response = document_status.update_document_status(id,Document_Status)
    return response