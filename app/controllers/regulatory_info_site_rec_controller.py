from typing import List
from fastapi import APIRouter, Depends
from app.services.regulatory_info_site_rec_service import Regulatory_Info_Service
from app.schemas.regulatory_info_site_rec import Regulatory_Information,Documents_List,Update_Regulatory_Information

router = APIRouter(prefix="/api")
regulatory_info_service = Regulatory_Info_Service()

# @router.post("/regulatory-info")
# def add_regulatory_info_details(regulatory_info:Regulatory_Information,update_reg_info:Update_Regulatory_Information):
#     # response = regulatory_info_service.add_regulatory_info_details(regulatory_info)
#     response = regulatory_info_service.add_or_update_regulatory_info_details(regulatory_info,update_reg_info)
#     return response

# This is a delicate method to implement.Single line error leads to entire pipeline to be broken.The same for loop can be looped in services file too.

@router.post("/regulatory-info")
def add_and_update_regulatory_info(regulatory_info: Regulatory_Information):
    for document in regulatory_info.documents:
        if document.site_rec_reg_info_id is not None and document.site_rec_reg_info_id !=0:
            update_reg_info = Update_Regulatory_Information(
                document=document.document,
                availability=document.availability,
                date=document.date,
                remarks=document.remarks,
                updated_by_id=document.updated_by_id
            )
            site_rec_reg_info_id = document.site_rec_reg_info_id
            response = regulatory_info_service.update_regulatory_info_details(site_rec_reg_info_id,update_reg_info,regulatory_info)
        elif document.site_rec_reg_info_id == 0:
            new_reg_info = Regulatory_Information(
                site_id=regulatory_info.site_id,
                documents=[document],   
                created_by_id=regulatory_info.created_by_id
            )
            response = regulatory_info_service.add_regulatory_info_details(new_reg_info)
    return response




@router.get("/regulatory-info")
def get_regulatory_info_details():
    response = regulatory_info_service.get_all_regulatory_info_details()
    return response

@router.get("/regulatory-info/{site_id}")
def get_regulatory_info_by_site_id(site_id:int):
    response = regulatory_info_service.get_regulatory_info_details_by_site_id(site_id)
    return response

@router.delete("/regulatory-info/{site_id}/{site_rec_reg_info_id}")
def delete_regulatory_info_by_site_id_and_site_rec_reg_info_id(site_id:int,site_rec_reg_info_id:int):
    response = regulatory_info_service.delete_regulatory_info_details_by_site_id_and_site_rec_reg_info_id(site_id,site_rec_reg_info_id)
    return response

# @router.put("/regulatory-info/{site_id}/{document_category_id}")
# def update_regulatory_info_by_site_id_and_document_id(site_id:int ,document_category_id:int,reg_info:Update_Regulatory_Information):
#     response = regulatory_info_service.update_regulatory_info_details_by_site_id_and_document_id(site_id,document_category_id,reg_info)
#     return response
