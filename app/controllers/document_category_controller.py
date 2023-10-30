from fastapi import APIRouter, Depends
from app.schemas.document_category_schema import DocumentCategory,Updatedocumentcategory
from app.services.document_category_service import Document_Category_Service
router = APIRouter(prefix="/api")
document_category_service = Document_Category_Service()
@router.post("/documentcategory")
def add_document_category(document_details : DocumentCategory):
    response = document_category_service.add_document_category(document_details)
    return response
# @router.get("/documentcategory")
# def get_document_category():
#     response = document_category_service.document_category_list()
#     return response

# get data by org, taking user_id as input paramter
@router.get("/alldocumentcategories/{user_id}")
def get_all_document_categories_related_to_org(user_id:int):
    response = document_category_service.document_category_list(user_id)
    return response

@router.put("/documentcategory/{id}")
def update_document_category(id:int,DocumentCategory:Updatedocumentcategory):
    response = document_category_service.update_document(id,DocumentCategory)
    return response
@router.get("/documentcategory/{id}")
def get_document_category(id:int):
    response = document_category_service.get_document_category(id)
    return response    
