from typing import List
from fastapi import APIRouter, Depends
from app.schemas.population_group_schema import Population_Group, Update_Population_Group
from app.services.population_group_service import Population_Group_Service

router = APIRouter(prefix="/api")
population_group_service = Population_Group_Service()

@router.post("/populationgroup")
def add_population_group(data:Population_Group):
    response = population_group_service.add_population_group(data)
    return response

# @router.get("/populationgroup")
# def get_population_groups():
#     response = population_group_service.get_population_groups()
#     return response
# get data by org, taking user_id as input paramter
@router.get("/allpopulationgroups/{user_id}")
def get_population_groups_related_org(user_id:int):
    response = population_group_service.get_population_groups(user_id)
    return response

@router.get("/populationgroup/{id}")
def get_population_group(id:int):
    response = population_group_service.get_population_group(id)
    return response        

@router.put("/populationgroup/{id}")
def update_population_group(id:int,data:Update_Population_Group):
    response = population_group_service.update_population_group(id,data)
    return response    