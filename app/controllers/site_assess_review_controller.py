from typing import List
from fastapi import APIRouter,Depends
from app.schemas.site_assess_review_schema import Site_Assess_Review, details, Update_Site_Assess_Review
from app.services.site_assess_review_service import  Site_Assess_Review_Service

router = APIRouter(prefix="/api")
site_assess_review_service  = Site_Assess_Review_Service()

@router.post("/siteassessreview")
def add_site_assess_review(data : Site_Assess_Review):
    response = site_assess_review_service.add_site_assess_review(data)
    return response

@router.get("/evalutationmodes")
def get_evalutation_modes():
    response = site_assess_review_service.get_evalutation_modes()
    return response

@router.get("/siteassessreview/{id}")
def get_site_assess_review(id:int):
    response = site_assess_review_service.get_site_assess_review(id)
    return response     

@router.put("/siteassessreview/{id}")
def update_site_assess_review(id:int,data:Update_Site_Assess_Review):
    response = site_assess_review_service.update_site_assess_review(id,data)
    return response     

@router.delete("/siteassessreview/{id}")
def delete_reviewer(id:int):
    response = site_assess_review_service.delete_reviewer(id)
    return response     