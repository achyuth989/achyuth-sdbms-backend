from typing import List
from fastapi import APIRouter, Depends
from app.services.site_asmt_infrastructure_service import Site_Asmt_Infra_Service
from app.schemas.site_asmt_infrastructure import Site_Asmt_Infrastructure,Infra_Questionary_List,Update_Site_Asmt_Infra

router = APIRouter(prefix="/api")
site_asmt_infra_service = Site_Asmt_Infra_Service()

# @router.post("/asmt-infrastructure")
# def add_site_asmt_infrastructure_details(site_asmt_infra:Site_Asmt_Infrastructure):
#     response = site_asmt_infra_service.add_asmt_infra_details(site_asmt_infra)
#     return response

@router.get("/asmt-infrastructure/{site_id}")
def get_site_asmt_infrastructure_details_by_site_id(site_id:int):
    response = site_asmt_infra_service.get_asmt_infra_details_by_site_id(site_id)
    return response


@router.get("/asmt-infrastructure")
def get_all_asmt_infrastructure_details():
    response = site_asmt_infra_service.get_all_asmt_infra_details()
    return response


# This is a delicate method to implement.Single line error leads to entire pipeline to be broken.The same for loop can be looped in services file too.
# Instead of looping in controller file,we can also loop the same code in services file too

@router.post("/asmt-infrastructure")
def add_and_update_site_asmt_infrastructure_details(site_asmt_infra:Site_Asmt_Infrastructure):
    for questions in site_asmt_infra.questionaries:
        if questions.site_asmt_infra_equal_id is not None and questions.site_asmt_infra_equal_id !=0:
            update_asmt_infra = Update_Site_Asmt_Infra(
                question = questions.question,
                answer = questions.answer,
                input = questions.input,
                updated_by_id = questions.updated_by_id
            )
            site_asmt_infra_equal_id = questions.site_asmt_infra_equal_id
            response = site_asmt_infra_service.update_asmt_infra_details(site_asmt_infra_equal_id,update_asmt_infra,site_asmt_infra)
        elif questions.site_asmt_infra_equal_id == 0:
            new_site_asmt_infra = Site_Asmt_Infrastructure(
                site_id = site_asmt_infra.site_id,
                questionaries = [questions],
                created_by_id=site_asmt_infra.created_by_id
            )
            response = site_asmt_infra_service.add_asmt_infra_details(new_site_asmt_infra)
    return response
            


