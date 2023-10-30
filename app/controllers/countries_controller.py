from typing import List
from fastapi import APIRouter, Depends
from app.services.countries_service import Countries_Service

router = APIRouter(prefix="/api")
countries_service = Countries_Service()

@router.get("/countries")
def get_country_details():
    response  =  countries_service.get_country_details()
    return response 

@router.get("/countries/{id}")
def country_details(id:int):
    response  =  countries_service.country_details(id)
    return response     