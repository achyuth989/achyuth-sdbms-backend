from typing import List
from fastapi import APIRouter, Depends
from app.schemas.address_schema import Address
from app.services.address_service import Address_Service

router = APIRouter(prefix="/api")
address_service = Address_Service()

@router.post("/address")
def add_address(data:Address):
    response  =  address_service.add_address(data)
    return response 

@router.get("/address/{id}")
def get_address(id:int):
    response  =  address_service.get_address(id)
    return response     