from typing import List
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from app.schemas.general_schema import General, GeneralUpdate, FilterCr
from app.services.general_service import General_Service
import os
import pandas as pd
from sqlalchemy.orm import Session 
import logging
# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Create a logger
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api")
general_service = General_Service()

# @router.post("/post_general")
# def post_general(data: General):
#     response = general_service.post_general(data)
#     return response


@router.put("/put_general/{cr_general_id}")
def put_general(cr_general_id: int, data: General):
    response = general_service.put_general(cr_general_id, data)
    return response

@router.get("/get_site_crs/{site_id}")
def get_site_crs(site_id: int):
    response = general_service.get_site_crs(site_id)
    return response

@router.get("/getclinicalresearcher/{id}")
def get_cr_by_id(id: int):
    response = general_service.get_cr_by_id(id)
    return response

@router.get("/get_all_crs")
def get_all_crs():
    response = general_service.get_all_crs()
    return response

@router.get("/clinicalresearchers/{org_id}")
def get_crs(org_id : int):
    response = general_service.get_crs(org_id)
    return response

@router.delete("/delete_edu/{cr_gen_edu_id}")
def delete_general_education(cr_gen_edu_id:int):
    response = general_service.delete_gen_edu(cr_gen_edu_id)
    return response

@router.delete("/delete_fac/{cr_gen_fac_aff_id}")
def delete_general_facilities(cr_gen_fac_aff_id:int):
    response = general_service.delete_gen_fac(cr_gen_fac_aff_id)
    return response

@router.post("/filtercrs")
def filter_cr(data:FilterCr):
    response = general_service.filter_cr(data)
    return response    

# @router.get("/get_general_by_siteid_and_sitereccrid/{site_id}/{site_rec_cr_id}")
# def get_general_by_siteid_and_sitereccrid(site_id: int, site_rec_cr_id: int):
#     response = general_service.get_by_site_id_and_site_rec_cr_id(site_id, site_rec_cr_id)
#     return response

def is_valid_file(filename: str):
        return filename.endswith(('.csv', '.xlsx','.xls'))
    
    
def save_uploaded_file(file: UploadFile):
        filename = os.path.basename(file.filename)
        os.makedirs("temp", exist_ok=True)
        temp_file_path = os.path.join("temp", filename)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.file.read())        
        return temp_file_path
    
@router.post("/multiple-cr-upload/{id}/{site_id}")
async def upload_file(file: UploadFile, id:int, site_id:int):
    if not is_valid_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # Save the uploaded file to a temporary location
    temp_file_path = save_uploaded_file(file)
    print("Temporary file path:", temp_file_path)
    response = general_service.multiple_cr_upload(temp_file_path,id,site_id)
    return response
    # except Exception as e:
    #     logger.error("Error occurred during processing:", exc_info=True)
    #     print("Error:", str(e))
    #     return {"error": "Error occurred while uploading and processing the data"}
