from typing import List
from fastapi import APIRouter, Depends
from app.services.audit_log_service import Audit_Log_Service
from app.schemas.general_schema import Reason

router = APIRouter(prefix="/api")
audit_log_service = Audit_Log_Service()


@router.get("/recoginitionauditlog/{id}")
def get_recognition_audit_log(id:int):
    response  =  audit_log_service.get_recognition_audit_log(id)
    return response     

@router.get("/assessmentauditlog/{id}")
def get_assessment_audit_log(id:int):
    response  =  audit_log_service.get_assessment_audit_log(id)
    return response         

@router.get("/clinicalresearcherauditlog/{id}")
def get_cr_audit_log(id:int):
    response  =  audit_log_service.get_cr_audit_log(id)
    return response  

@router.post("/crauditlog")
def reason_for_blocking(data:Reason):
    response  =  audit_log_service.reason_for_blocking(data)
    return response                
