from fastapi import APIRouter, Depends 
from app.schemas.rec_population_grp_schema import Questions,Specialities,Rec_Population_Grp,Update_Rec_Population_Grp
from app.services.rec_population_grp_service import Rec_Population_Grp_Service
router = APIRouter(prefix="/api")
rec_population_grp_service = Rec_Population_Grp_Service()

@router.post("/recpopulationgroup")
def add_rec_population_grp(data : Rec_Population_Grp):
    response = rec_population_grp_service.add_rec_population_grp(data)
    return response

@router.get("/recpopulationgroup/{id}")
def get_rec_population_grp(id:int):
    response = rec_population_grp_service.get_rec_population_grp(id)
    return response    

@router.put("/recpopulationgroup/{id}")
def update_rec_population_grp(id:int,data:Update_Rec_Population_Grp):
    response = rec_population_grp_service.update_rec_population_grp(id,data)
    return response    

@router.delete("/recpopulationgroupspecialities/{site_id}/{id}")
def delete_rec_population_grp_specialities(site_id:int, id:int):
    response = rec_population_grp_service.delete_rec_population_grp_specialities(site_id,id)
    return response     