from app.model.user import User
from app.model.service_category import Service_Category
from app.model.services import Site_Services
from app.model.site_services import SiteServices
from app.model.service_category import Service_Category
from app.model.rec_population_grp import Rec_Population_grp
from app.model.questionnaire import Questionnaire
from app.model.study_type import Study_Type
from app.model.study_type import Study_Type
from app.model.site_assess_registration import Site_Assess_Registration
from app.model.miscellaneous import Miscellaneous
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc,not_,asc,Integer
from sqlalchemy.orm import aliased



class Site_Assess_Registration_Service:
    def add_site_assess_registration(self,data):
        db = next(get_db())
        site_id = db.query(Site_Assess_Registration).filter(Site_Assess_Registration.site_id == data.site_id).first()
        if(site_id):
            return{"response":"registration data already exists"}
        else:    
            try:
                Miscellaneous_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == data.experience_in_studies).scalar()
                new_registration= Site_Assess_Registration(
                    site_id = data.site_id,
                    experience_in_studies = Miscellaneous_id,
                    created_by_id = data.created_by_id
                )
                db.add(new_registration)
                db.commit()

                for service in data.category_services:
                    new_category=Site_Assess_Registration(
                        site_id = data.site_id,
                        category_id = service.category_id,
                        services = service.services,
                        created_by_id = data.created_by_id
                    )
                    db.add(new_category)
                    db.commit()


                for question in data.questions:
                    questions_id = db.query(Questionnaire).filter(Questionnaire.question == question.question).first()
                    question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()
                    if question.answer :
                        study_type = db.query(Study_Type).filter(Study_Type.studytype_id == question.answer).first()
                    if questions_id.type == "multi choice" :
                        new_question = Site_Assess_Registration(
                            site_id = data.site_id,
                            question = questions_id.questionnaire_id,
                            input = study_type.studytype_id,
                            created_by_id = data.created_by_id
                        )
                        db.add(new_question)
                        db.commit()
                    else:
                            new_question = Site_Assess_Registration(
                                site_id = data.site_id,
                                question = questions_id.questionnaire_id,
                                input = question.answer,
                                created_by_id = data.created_by_id
                            )
                            db.add(new_question)
                            db.commit()
                    
                return{"response":"registration data added successfully"}    
            finally:
                db.close()

    # def get_site_assess_registration(self,id):
    #     db = next(get_db())
    #     try:
    #         experience_in_studies = db.query(Site_Assess_Registration.experience_in_studies,Site_Assess_Registration.site_asmt_reg_ser_id)\
    #         .filter(Site_Assess_Registration.site_id == id)\
    #         .filter(Site_Assess_Registration.experience_in_studies != "").first()

    #         services = db.query(Site_Assess_Registration.services,Service_Category.description,Service_Category.service_category_id,Site_Assess_Registration.site_asmt_reg_ser_id)\
    #         .join(Service_Category,Service_Category.service_category_id == Site_Assess_Registration.category_id).filter(Site_Assess_Registration.site_id == id).all()

    #         questions = db.query(Site_Assess_Registration.input,Site_Assess_Registration.site_asmt_reg_ser_id,Questionnaire.question,Questionnaire.questionnaire_id)\
    #         .join(Questionnaire,Site_Assess_Registration.question == Questionnaire.questionnaire_id)\
    #         .filter(Site_Assess_Registration.site_id == id).filter(Site_Assess_Registration.experience_in_studies.is_(None)).all()
            
    #         registration_data = {}
    #         registration_data['experience_in_studies'] = experience_in_studies
    #         registration_data['category_services'] = services
    #         registration_data['questions'] = questions

    #         return registration_data
    #     finally:
    #         db.close()    
    
    def get_site_assess_registration(self,id):
        db = next(get_db())
        try:
            experience_in_studies = db.query(Site_Assess_Registration.input,Site_Assess_Registration.category_id,Site_Assess_Registration.created_by_id,Site_Assess_Registration.updated_by_id,Site_Assess_Registration.site_id,Site_Assess_Registration.question,Site_Assess_Registration.services,Site_Assess_Registration.site_asmt_reg_ser_id,Site_Assess_Registration.experience_in_studies,Miscellaneous.value,Miscellaneous.miscellaneous_id)\
            .join(Miscellaneous,Miscellaneous.miscellaneous_id == Site_Assess_Registration.experience_in_studies)\
            .filter(Site_Assess_Registration.site_id == id).first()
     
            
            input_data =  db.query(Site_Assess_Registration.input,Site_Assess_Registration.site_asmt_reg_ser_id,Questionnaire.question,Questionnaire.questionnaire_id)\
            .join(Questionnaire,Site_Assess_Registration.question == Questionnaire.questionnaire_id)\
            .filter(Site_Assess_Registration.site_id == id).filter(Site_Assess_Registration.experience_in_studies.is_(None)).first()
            

            services = db.query(Site_Assess_Registration.services,Service_Category.description,Service_Category.service_category_id,Site_Assess_Registration.site_asmt_reg_ser_id)\
            .join(Service_Category,Service_Category.service_category_id == Site_Assess_Registration.category_id).filter(Site_Assess_Registration.site_id == id).all()
            
            
            distinct_site_asmt_reg_ser_ids = db.query(
                Site_Assess_Registration.site_asmt_reg_ser_id
            ).filter(
                Site_Assess_Registration.site_id == id,
                Site_Assess_Registration.experience_in_studies.is_(None)
            ).distinct()
            
            questions = db.query(Study_Type.study_type,Study_Type.study_type_id,Study_Type.description,Site_Assess_Registration.input, Site_Assess_Registration.site_asmt_reg_ser_id, Questionnaire.question, Questionnaire.questionnaire_id) \
            .join(Questionnaire, Site_Assess_Registration.question == Questionnaire.questionnaire_id) \
            .outerjoin(Study_Type, Site_Assess_Registration.input.cast(Integer) == Study_Type.studytype_id) \
            .filter(Site_Assess_Registration.site_asmt_reg_ser_id.in_(distinct_site_asmt_reg_ser_ids)).first()

            
            my_list = []
            my_list.append(questions)
            my_list.append(input_data)
            
            registration_data = {}
            registration_data['experience_in_studies'] = experience_in_studies
            registration_data['category_services'] = services
            registration_data['question'] = my_list
            return registration_data
        finally:
            db.close()    


    def update_site_assess_registration(self,id,data):
        db = next(get_db())   
        try:
            studies = db.query(Site_Assess_Registration)\
            .filter(Site_Assess_Registration.site_id == id).first()
            experience = db.query(Site_Assess_Registration).join(Miscellaneous, Site_Assess_Registration.experience_in_studies == Miscellaneous.miscellaneous_id).filter(Site_Assess_Registration.site_id == id).all()
            Miscellaneous_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == data.experience_in_studies).scalar()
            if(studies):
                studies.experience_in_studies =Miscellaneous_id
                studies.updated_by_id = data.updated_by_id
            else:
                new_registration= Site_Assess_Registration(
                    site_id = id,
                    experience_in_studies = Miscellaneous_id,
                    created_by_id = data.updated_by_id
                )
                db.add(new_registration)
                db.commit()

            db.commit()   

            questions = db.query(Site_Assess_Registration)\
            .join(Questionnaire,Site_Assess_Registration.question == Questionnaire.questionnaire_id)\
            .filter(Site_Assess_Registration.site_id == id).all()

            count = 0
            for question in data.questions:
                    questions_id = db.query(Questionnaire).filter(Questionnaire.question == question.question).first()
                    question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()
                    if question.answer :
                        study_type = db.query(Study_Type).filter(Study_Type.studytype_id == question.answer).first()
                        index = None
                        for i, q in enumerate(questions):
                            if q.question == question_id[0]:
                                index = i
                                break
                        if index is not None:
                            # Update the existing question
                            questions[index].input = question.answer
                            questions[index].updated_by_id = data.updated_by_id
                        else:
                            if questions_id.type == "multi choice" :
                                new_question = Site_Assess_Registration(
                                    site_id = id,
                                    question = questions_id.questionnaire_id,
                                    input = study_type.studytype_id,
                                    created_by_id = data.updated_by_id
                                )
                                db.add(new_question)
                                db.commit()
                            else:
                                    new_question = Site_Assess_Registration(
                                        site_id = id,
                                        question = questions_id.questionnaire_id,
                                        input = question.answer,
                                        created_by_id = data.updated_by_id
                                    )
                                    db.add(new_question)
                                    db.commit()
                            count+=1
                            

            services = db.query(Site_Assess_Registration)\
            .filter(Site_Assess_Registration.site_id == id)\
            .filter(Site_Assess_Registration.category_id != 0).all()

            ser_count = 0
            for service in data.category_services:
                if ser_count < len(services):
                    services[ser_count].category_id = service.category_id
                    services[ser_count].services = service.services
                    services[ser_count].updated_by_id = data.updated_by_id
                else:
                    new_service = Site_Assess_Registration(site_id=id, category_id=service.category_id, services=service.services, created_by_id=data.updated_by_id)
                    db.add(new_service)
                ser_count += 1
            db.commit()
            return{"response":"Registration data updated successfully"}

        finally:
            db.close()
    