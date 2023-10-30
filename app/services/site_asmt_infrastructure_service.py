from app.model.site_asmt_infrastructure import SiteAsmtInfrastructure
from app.schemas.site_asmt_infrastructure import Site_Asmt_Infrastructure,Infra_Questionary_List,Update_Site_Asmt_Infra
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func

class Site_Asmt_Infra_Service:
    def add_asmt_infra_details(self,site_asmt_infra):
        db= next(get_db())  
        try:
            for questions in site_asmt_infra.questionaries:
                actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                answers = questions.answer
                answer_record = db.query(Miscellaneous).filter(Miscellaneous.value == answers).first()
                answer_id = answer_record.miscellaneous_id
                if actual_question_record:
                    question_id = actual_question_record.questionnaire_id
                    
                    new_site_asmt_infra=SiteAsmtInfrastructure(
                        site_id = site_asmt_infra.site_id,
                        question =question_id,
                        answer = answer_id,
                        input = questions.input,
                        created_by_id = site_asmt_infra.created_by_id
                    )
                    db.add(new_site_asmt_infra)
                    db.commit()
                    db.refresh(new_site_asmt_infra)
                else:
                    return "Invalid question"
            return "Site Assessment details added successfully"
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
    
    
    def get_asmt_infra_details_by_site_id(self,site_id):
        db = next(get_db())
        try:
            asmt_infra_site_details = db.query(SiteAsmtInfrastructure).filter(SiteAsmtInfrastructure.site_id == site_id).all()
            for data in asmt_infra_site_details:
                question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
                answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
                if question_data is not None:
                    data.question_text = question_data.question
                    data.answer_text=answer_data.value
            return asmt_infra_site_details
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
        
            
    def get_all_asmt_infra_details(self):
        db = next(get_db())
        try:
            asmt_infra_site_details = db.query(SiteAsmtInfrastructure).all()
            for data in asmt_infra_site_details:
                question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
                answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
                if question_data is not None:
                    data.question_text=question_data.question
                    data.answer_text=answer_data.value
            return asmt_infra_site_details
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
            
    
    
    def update_asmt_infra_details(self,site_asmt_infra_equal_id:int,update_asmt_infra:Update_Site_Asmt_Infra,site_asmt_infra:Site_Asmt_Infrastructure):
        db = next(get_db())
        try:
            for questions in site_asmt_infra.questionaries:
                if questions.site_asmt_infra_equal_id == site_asmt_infra_equal_id:
                    update_asmt_infrastructure = db.query(SiteAsmtInfrastructure).filter(SiteAsmtInfrastructure.site_asmt_infra_equal_id == site_asmt_infra_equal_id).first()
                    
                    actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                    question_id = actual_question_record.questionnaire_id
                    
                    answers = questions.answer
                    answer_record = db.query(Miscellaneous).filter(Miscellaneous.value == answers).first()
                    answer_id = answer_record.miscellaneous_id
                    
                    
                    if update_asmt_infrastructure:
                        update_asmt_infrastructure.question = question_id
                        update_asmt_infrastructure.answer = answer_id
                        update_asmt_infrastructure.input = update_asmt_infra.input
                        update_asmt_infrastructure.updated_by_id = update_asmt_infra.updated_by_id
                        db.commit()
            return "Answer updated successfully"
                    
            # db.commit()
            # return "Answer_updated sucessfully"

            # return update_reg_info
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Site Assessment Infrastructure not found")
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
        finally:
            db.close()
            