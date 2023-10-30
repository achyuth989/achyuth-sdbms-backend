from typing import List
from fastapi import APIRouter, Depends
from app.schemas.research_product_schema import Research_Product, Update_Research_Product
from app.services.research_product_service import Research_Product_Service

router = APIRouter(prefix="/api")
research_product_service = Research_Product_Service()

@router.post("/researchproduct")
def add_research_product(data:Research_Product):
    response = research_product_service.add_research_product(data)
    return response

# @router.get("/researchproduct")
# def get_research_product():
#     response = research_product_service.get_research_product()
#     return response 
# get data by org, taking user_id as input paramter
@router.get("/researchproducts/{user_id}")
def get_research_products_related_to_org(user_id:int):
    response = research_product_service.get_research_product(user_id)
    return response 

@router.get("/researchproduct/{id}")
def get_research_product(id:int):
    response = research_product_service.research_product(id)
    return response        

@router.put("/researchproduct/{id}")
def update_research_product(id:int,data:Update_Research_Product):
    response = research_product_service.update_research_product(id,data)
    return response     