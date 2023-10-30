from app.model.cr_infra_site_rec import Cr_infra
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from app.model.study_phases import StudyPhases
from app.model.research_product import Research_Product
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func

class Cr_Infra_Service:
    def add_cr_infra_details(self,cr_infra):
        db = next(get_db())
        try:
            
            
            # Get the site_id of the newly inserted crinfo
            for questions in cr_infra.questionaries:
                # actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                # question_id = actual_question_record.questionnaire_id
                # answers = questions.answer
                # answer_record = db.query(Miscellaneous).filter(Miscellaneous.value == answers).first()
                # answer_id = answer_record.miscellaneous_id
                
                # check whether id exists or not
                
                existing_site_rec_cr_infra_id = questions.site_rec_cr_infra_id
                if existing_site_rec_cr_infra_id:
                    existing_cr_infra_record = db.query(Cr_infra).get(existing_site_rec_cr_infra_id)
                    if existing_cr_infra_record:
                        if questions.type == "yes":
                            
                            actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                            question_id = actual_question_record.questionnaire_id
                            answers = questions.answer
                            answer_record = db.query(Miscellaneous).filter(Miscellaneous.value == answers).first()
                            answer_id = answer_record.miscellaneous_id
                            
                            existing_cr_infra_record.question = question_id
                            existing_cr_infra_record.answer =answer_id
                            existing_cr_infra_record.updated_by_id = cr_infra.created_by_id
                            db.commit()
                            
                        
                        elif questions.type == "phase":
                            actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                            question_id = actual_question_record.questionnaire_id
                            
                            existing_cr_infra_record.question = question_id
                            existing_cr_infra_record.phase_study_ids = questions.answer
                            existing_cr_infra_record.updated_by_id = cr_infra.created_by_id
                            db.commit()
                        
                        elif questions.type == "research":
                            actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                            question_id = actual_question_record.questionnaire_id    
                            
                            existing_cr_infra_record.question = question_id
                            existing_cr_infra_record.research_product_ids = questions.answer
                            existing_cr_infra_record.updated_by_id = cr_infra.created_by_id
                            db.commit()

                    else:
                        return f"site_rec_cr_infra_id={site_rec_cr_infra_id} is invalid(questionaries), Please pass 0 to add new record to db or send appropriate id to edit the same record"
                        
                   
                else:
                    if questions.type == "yes":
                        
                        actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                        question_id = actual_question_record.questionnaire_id
                        answers = questions.answer
                        answer_record = db.query(Miscellaneous).filter(Miscellaneous.value == answers).first()
                        answer_id = answer_record.miscellaneous_id
                        
                        
                        new_cr_infra = Cr_infra(
                            site_id = cr_infra.site_id,
                            question = question_id,
                            answer =answer_id,
                            updated_by_id = questions.updated_by_id,
                            created_by_id = cr_infra.created_by_id
                        )
                        db.add(new_cr_infra)
                        db.commit()
                        db.refresh(new_cr_infra)
                    elif questions.type == "phase":
                        # new_cr_infra = "phase"
                        
                        actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                        question_id = actual_question_record.questionnaire_id
                        
                        new_cr_infra = Cr_infra(
                            site_id = cr_infra.site_id,
                            question = question_id,
                            # answer =question.answer,
                            # questionaries=cr_infra.questionaries,
                            phase_study_ids = questions.answer,
                            updated_by_id = questions.updated_by_id,
                            created_by_id = cr_infra.created_by_id
                        )
                        db.add(new_cr_infra)
                        db.commit()
                        db.refresh(new_cr_infra)
                    elif questions.type == "research":
                        # new_cr_infra = "research"
                        actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == questions.question).first()
                        question_id = actual_question_record.questionnaire_id
                        new_cr_infra = Cr_infra(
                            site_id = cr_infra.site_id,
                            question = question_id,
                            # answer =question.answer,
                            # questionaries=cr_infra.questionaries,
                            # phase_studies_ids = cr_infra.phase_studies_ids,
                            research_product_ids = questions.answer,
                            updated_by_id = questions.updated_by_id,
                            created_by_id = cr_infra.created_by_id
                        )
                        db.add(new_cr_infra)
                        db.commit()
                        db.refresh(new_cr_infra)


            for data in cr_infra.research:
                phase_id = data.phase_id
                phase_id = int(phase_id)
                existing_site_rec_cr_infra_id = data.site_rec_cr_infra_id
                
                if existing_site_rec_cr_infra_id:
                    existing_cr_infra_record = db.query(Cr_infra).get(existing_site_rec_cr_infra_id)
                    if existing_cr_infra_record:
                        existing_cr_infra_record.study_name = data.study_name
                        existing_cr_infra_record.type_of_study = data.type_of_study
                        existing_cr_infra_record.phase_id = phase_id
                        existing_cr_infra_record.sponsor = data.sponsor
                        existing_cr_infra_record.no_of_patients_recruited = data.no_of_patients_recruited
                        existing_cr_infra_record.start_date =data.start_date
                        existing_cr_infra_record.end_date =data.end_date
                        existing_cr_infra_record.updated_by_id = cr_infra.created_by_id
                        db.commit()
                        
                    else:
                        return f"site_rec_cr_infra_id={site_rec_cr_infra_id} is invalid(clinical study research), Please pass 0 to add new record to db or send appropriate id to edit the same record"
                else:
                
                    new_cr_infra= Cr_infra(
                        site_id = cr_infra.site_id,
                        study_name = data.study_name,
                        type_of_study = data.type_of_study,
                        phase_id = phase_id,
                        sponsor = data.sponsor,
                        no_of_patients_recruited = data.no_of_patients_recruited,
                        start_date =data.start_date,
                        end_date =data.end_date,
                        updated_by_id = data.updated_by_id,
                        created_by_id = cr_infra.created_by_id                    
                    )
                    db.add(new_cr_infra)
                    db.commit()
                    db.refresh(new_cr_infra)
                    
            return "cr infra details added successfully"
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

  
            
    def get_cr_infra_details_by_site_id(self,site_id):
        db = next(get_db())
        try:
            cr_infra_site_details = db.query(Cr_infra).filter(Cr_infra.site_id == site_id).all()
            if cr_infra_site_details:
                questions_list =[]
                # questions_phase_list =[]
                research_list = []
                for details in cr_infra_site_details:
                    if details.answer is not None:
                        question_id = details.question
                        question_record = db.query(Questionnaire).filter(Questionnaire.questionnaire_id== question_id).first()
                        if question_record:
                            final_question = question_record.question
                            details.question = final_question
                        else:
                            details.question = None
                        
                        answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==details.answer).first()
                        if answer_record:
                            final_answer = answer_record.value
                            details.final_answer= final_answer
                        else:
                            details.final_answer = None
                        
                        q_a_pair = {
                            "site_rec_cr_infra_id":details.site_rec_cr_infra_id,
                            "site_id":details.site_id,
                            "question_id":question_id,
                            "answer_id":details.answer,
                            "question_record":final_question,
                            "answer_record":final_answer,
                            "type":"yes"
                        }
                        
                        questions_list.append(q_a_pair)
                        
                    elif details.phase_study_ids is not None:
                        question_id = details.question
                        question_record = db.query(Questionnaire).filter(Questionnaire.questionnaire_id== question_id).first()
                        final_question = question_record.question
                        
                        phase_study_ids_list = details.phase_study_ids.split(",")
                        phase_answer =[]
                        for ids in phase_study_ids_list:
                            ids = int(ids)
                            phase_answer_record = db.query(StudyPhases).filter(StudyPhases.study_phase_id == ids).first()
                            if phase_answer_record is not None:
                                answer = phase_answer_record.phases_type
                                phase_answer.append(answer)
                            else:
                                answer = None
                                phase_answer.append(answer)
                        question_record = {
                            "site_id":details.site_id,
                            "site_rec_cr_infra_id":details.site_rec_cr_infra_id,
                            "question":final_question,
                            "answer":phase_answer,
                            "type":"phase"
                        }
                        questions_list.append(question_record)
                        
                    elif details.research_product_ids is not None:
                        question_id = details.question
                        question_record = db.query(Questionnaire).filter(Questionnaire.questionnaire_id== question_id).first()
                        final_question = question_record.question
                        
                        research_product_ids_list = details.research_product_ids.split(",")
                        research_answer =[]
                        for ids in research_product_ids_list:
                            ids = int(ids)
                            research_answer_record = db.query(Research_Product).filter(Research_Product.research_product_id == ids).first()
                            if research_answer_record:
                                answer = research_answer_record.research_product_type
                                research_answer.append(answer)
                            else:
                                answer = None
                                research_answer.append(answer)
                            
                        question_record = {
                            "site_id":details.site_id,
                            "site_rec_cr_infra_id":details.site_rec_cr_infra_id,
                            "question":final_question,
                            "answer":research_answer,
                            "type":"research"
                        }
                        questions_list.append(question_record)
                        
                    elif details.study_name is not None:
                        research_record = {
                            "site_id":details.site_id,
                            "site_rec_cr_infra_id":details.site_rec_cr_infra_id,
                            "study_name":details.study_name,
                            "type_of_study":details.type_of_study,
                            "phase_id":details.phase_id,
                            "sponsor":details.sponsor,
                            "no_of_patients_recruited": details.no_of_patients_recruited,
                            "start_date":details.start_date,
                            "end_date":details.end_date,
                            "created_by_id":details.created_by_id
                                
                        }

                        research_list.append(research_record)
                 
                return {"questions":questions_list,"research":research_list}
                        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
        finally:
            db.close()
          
          
    def delete_cr_infra_details_by_site_id_and_cr_infra_id(self,site_id,site_rec_cr_infra_id):
        db = next(get_db()) 
        try:
            cr_infra_site_details = db.query(Cr_infra).filter(Cr_infra.site_id == site_id).filter(Cr_infra.site_rec_cr_infra_id == site_rec_cr_infra_id).first()
            if cr_infra_site_details:
                db.delete(cr_infra_site_details)
                db.commit()
                return "cr_infra_site_details deleted successfully"
            else:
                return f"site_id={site_id} or site_rec_cr_infra_id = {site_rec_cr_infra_id} is invalid"
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()      
                    
                    
                