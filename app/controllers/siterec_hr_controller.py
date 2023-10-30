from typing import List
from fastapi import  APIRouter,Depends
from app.model.site_rec_hr  import Siterec_hr
from app.schemas.siterec_hr_schema import Sitehr,Updatesitehr
from app.services.siterec_hr_service import  Site_rec_hr

router = APIRouter(prefix="/api")
siterec_hr  = Site_rec_hr()


@router.post("/siterechr")
def Add_siterec_hr(records:Sitehr):
    response = siterec_hr.post_siterec_hr(records)
    return response

@router.get("/siterechr")
def Get_siterec_hr():
    response = siterec_hr.get_siterec_hr()
    return response

@router.get("/siterechr/{side_id}")
def Get_icd_siteid(side_id:int):
    response = siterec_hr.get_sitehr_by_id(side_id)
    return response

@router.put("/siterechr/{site_id}")
def update_site_hr(site_id:int,records:Updatesitehr):
    response = siterec_hr.update_sitehr(site_id,records)
    return response

@router.delete("/siterechr/{id}")
def delete_icd_md(id:int):
    response = siterec_hr.get_delete_hrservice(id)
    return response

