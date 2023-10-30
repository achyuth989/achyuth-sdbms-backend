from typing import List
from fastapi import APIRouter, Depends
from app.schemas.geography_schema import Geography, Update_Geography, Municipalities, Update_Municipality
from app.services.geography_service import Geography_Service


router = APIRouter(prefix="/api")
geography_service = Geography_Service()

@router.post("/geography")
def add_geography(data: Geography):
    response  =  geography_service.add_geography(data)
    return response

@router.get("/geography")
def get_all_geography():
    response = geography_service.get_geographies()
    return response    

@router.get("/geographymuncipalitiesmuni/{id}")
def get_all_geography(id:int):
    response = geography_service.get_geography_municplaities(id)
    return response  
@router.get("/geographycountriesmuni")
def get_all_geocountries():
    response = geography_service.get_geography_countries()
    return response  
@router.get("/geographystatesmuni/{id}")
def get_all_geostates(id:int):
    response = geography_service.get_geography_states(id)
    return response   

@router.get("/geography/{geography_id}/{city_id}")
def get_geography(geography_id:int,city_id:int):
    response = geography_service.get_geography(geography_id,city_id)
    return response      

@router.put("/geography/{id}")
def update_geography(id:int,data:Update_Geography):
    response = geography_service.update_geography(id,data)
    return response     

@router.get("/cities/{id}")
def get_cities(id:str):
    response = geography_service.get_cities(id)
    return response     

@router.get("/states/{id}")
def get_states(id:str):
    response = geography_service.get_states(id)
    return response   

@router.get("/municipalities/{country_state_id}")
def get_municipalities(country_state_id:str):
    response = geography_service.get_municipalities(country_state_id)
    return response 

@router.post("/municipalities")
def add_municipalities(data: Municipalities):
    response  =  geography_service.add_municipalities(data)
    return response  

# @router.get("/municipalities")
# def get_added_municipalities():
#     response = geography_service.get_added_municipalities()
#     return response
# get data by org, taking user_id as input paramter
@router.get("/allmunicipalities/{user_id}")
def get_added_by_municipalities_by_org(user_id:int):
    response = geography_service.get_added_municipalities(user_id)
    return response

@router.put("/municipalities/{id}")
def update_municipality(id:int,data:Update_Municipality):
    response = geography_service.update_municipality(id,data)
    return response     
