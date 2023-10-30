from typing import List
from fastapi import  APIRouter,Depends
from app.schemas.service_category_schema import Service_Category,Updateservicecategory
from app.services.service_category_service import Service_Categories

router = APIRouter(prefix="/api")
service_category  = Service_Categories()


@router.post("/servicecategory")
def Add_Service_category(data: Service_Category):
      response = service_category.Service_Category_Service(data)
      return response



# @router.get("/servicecategory")
# def Get_Service_categories_all():
#       response = service_category.get_Service_Category_all()
#       return response

# get data by org, taking user_id as input paramter
@router.get("/allservicecategories/{user_id}")
def Get_Service_categories_all(user_id:int):
      response = service_category.get_Service_Category_all(user_id)
      return response



@router.get("/servicecategory/{id}")
def categories_by_id(id:int):
      response = service_category.get_Service_Category_by_id(id)
      return response

@router.put("/servicecategory/{id}")
def update_service_category(id:int,Service_Category:Updateservicecategory):
      response = service_category.update_service_category(id,Service_Category)
      return response

