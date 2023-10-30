from fastapi import APIRouter, Depends
from app.services.site_recognition_service import Site_Recognition
router = APIRouter(prefix="/api")
site_recognition_service = Site_Recognition()

@router.get("/sitesrecognitions/{user_id}")

def get_sites_rec(user_id:int):
    response  =  site_recognition_service.sites_rec_list(user_id)
    return response

@router.get("/searchrecognitions")

def search_sites_rec(site_id:int=None , site_rec_status:int = None):
    response  =  site_recognition_service.search_sites_rec(site_id,site_rec_status)
    return response

@router.get("/miscellaneous")
def miscellaneous_sites_rec():
    response  =  site_recognition_service.miscellaneous_sites_rec()
    return response

@router.get("/miscellaneous/{mis_type}")
def miscellaneous_sites_by_type(mis_type:str):
    response  =  site_recognition_service.miscellaneous_sites_by_type(mis_type)
    return response

@router.get("/siteassessmentstatus/{user_id}")
def get_sites_assess_status(user_id:int):
    response  =  site_recognition_service.get_sites_assess_status(user_id)
    return response

@router.get("/clinicalresearcherstatus")

def get_cr_status():
    response  =  site_recognition_service.get_cr_status()
    return response        