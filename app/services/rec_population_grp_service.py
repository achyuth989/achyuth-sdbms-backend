from app.model.user import User
from app.model.rec_population_grp import Rec_Population_grp
from app.model.questionnaire import Questionnaire
from app.model.speciality_subspeciality import SpecialitySubspeciality
from app.model.specialities_subspecialities import Specalitiess

from app.model.speciality import Speciality
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc,not_,asc

class Rec_Population_Grp_Service:
    def add_rec_population_grp(self,data):
        db = next(get_db())
        site_id = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == data.site_id).first()
        if(site_id):
            return{"response":"Population group data already exists"}
        else:
            try:
                new_population_grp = Rec_Population_grp(
                    site_id = data.site_id,
                    pop_service_on_site_id = data.population_served,
                    created_by_id = data.created_by_id
                )
                db.add(new_population_grp)     
                db.commit() 
                for question in data.questions:
                    question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()
                    new_question = Rec_Population_grp(
                        site_id = data.site_id,
                        question = question_id[0],
                        input = question.answer,
                        created_by_id = data.created_by_id
                    )
                    db.add(new_question)
                    db.commit()
                for speciality in data.specialities:
                    for question in speciality.questions:
                        question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()
                        new_speciality = Rec_Population_grp(
                            site_id = data.site_id,
                            specialities_subspecialities_id = speciality.specialities,
                            question = question_id[0],
                            input = question.answer,
                            created_by_id = data.created_by_id
                        )
                        db.add(new_speciality)
                        db.commit()
                return{"response":"Population data Added Successfully"}    
            finally:
                db.close()      

    def get_rec_population_grp(self,id):
        db = next(get_db())
        try:
            complete_object = {}
            population_served = db.query(Rec_Population_grp.pop_service_on_site_id).filter(Rec_Population_grp.site_id == id).filter(Rec_Population_grp.pop_service_on_site_id != {}).first()

            if(population_served):
                population_list = list(map(int, population_served[0]))
                complete_object['population_served'] = population_list
            else:
                complete_object['population_served'] = []

            questions = db.query(Rec_Population_grp.input,Questionnaire.question,Questionnaire.questionnaire_id)\
            .join(Questionnaire,Rec_Population_grp.question == Questionnaire.questionnaire_id)\
            .filter(Rec_Population_grp.site_id == id).filter(Rec_Population_grp.specialities_subspecialities_id.is_(None)).all()

            if(questions):
                complete_object['questions'] = questions
            else:
                complete_object['questions'] = []    

            specialities = db.query(Rec_Population_grp.site_rec_pop_grp_id,Rec_Population_grp.specialities_subspecialities_id,Rec_Population_grp.input,SpecialitySubspeciality.speciality_id,SpecialitySubspeciality.subspeciality,Questionnaire.question,Questionnaire.questionnaire_id,Speciality.speciality)\
            .join(Questionnaire,Rec_Population_grp.question == Questionnaire.questionnaire_id)\
            .join(Specalitiess, Rec_Population_grp.specialities_subspecialities_id == Specalitiess.specialities_subspecialities_id)\
            .join(SpecialitySubspeciality,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
            .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
            .filter(Rec_Population_grp.site_id == id) \
            .order_by(asc(Rec_Population_grp.site_rec_pop_grp_id))\
            .all()

            if(specialities):

                def split_objects_into_pairs(objects):
                    pairs = [objects[i:i+2] for i in range(0, len(objects), 2)]
                    return pairs
                result = split_objects_into_pairs(specialities)

                complete_object['specialities'] = result
            else:
                complete_object['specialities'] = []
                
            return complete_object
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_rec_population_grp(self,id,data):
        db = next(get_db())   
        try:
            population_served = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == id).filter(Rec_Population_grp.pop_service_on_site_id != {}).first()
            pop_questions = db.query(Rec_Population_grp)\
            .join(Questionnaire,Rec_Population_grp.question == Questionnaire.questionnaire_id)\
            .filter(Rec_Population_grp.site_id == id).filter(Rec_Population_grp.specialities_subspecialities_id.is_(None)).all()

            if(population_served):
                population_served.pop_service_on_site_id = data.population_served
                population_served.updated_by_id = data.updated_by_id
            else:
                new_population_grp = Rec_Population_grp(
                    site_id = id,
                    pop_service_on_site_id = data.population_served,
                    created_by_id = data.updated_by_id
                )
                db.add(new_population_grp)     
                db.commit()     
            db.commit() 

            count = 0
            for question in data.questions:
                question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()
                if count < len(pop_questions):
                    # Update existing question
                    pop_questions[count].question = question_id[0]
                    pop_questions[count].input = question.answer
                    pop_questions[count].updated_by_id = data.updated_by_id
                else:
                    # Insert new question
                    new_question = Rec_Population_grp(site_id=id, question=question_id[0], input=question.answer, created_by_id=data.updated_by_id)
                    db.add(new_question)
                    db.commit()
                count += 1

            pop_specialities = db.query(Rec_Population_grp)\
            .join(SpecialitySubspeciality, Rec_Population_grp.specialities_subspecialities_id == SpecialitySubspeciality.id)\
            .join(Questionnaire,Rec_Population_grp.question == Questionnaire.questionnaire_id)\
            .filter(Rec_Population_grp.site_id == id) \
            .order_by(asc(Rec_Population_grp.site_rec_pop_grp_id))\
            .all()
            
            # spec_count = 0
            # for speciality in data.specialities:
            #     for question in speciality.questions:
            #         spec_question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()

            #         if spec_count < len(pop_specialities):
            #             pop_specialities[spec_count].specialities_subspecialities_id = speciality.specialities
            #             pop_specialities[spec_count].question = spec_question_id[0]
            #             pop_specialities[spec_count].input = question.answer
            #             pop_specialities[spec_count].updated_by_id = data.updated_by_id
            #             spec_count += 1
            #         else:
            #             new_speciality = Rec_Population_grp(site_id=id,specialities_subspecialities_id=speciality.specialities, question=spec_question_id[0], input=question.answer, created_by_id = data.updated_by_id)
            #             db.add(new_speciality)
            #         # spec_count += 1

            # db.commit()

            for speciality in data.specialities:
                for question in speciality.questions:
                    spec_question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()

                    if question.incrementid == 0:
                        new_speciality = Rec_Population_grp(
                            site_id=id,
                            specialities_subspecialities_id=speciality.specialities,
                            question=spec_question_id[0],
                            input=question.answer,
                            created_by_id=data.updated_by_id
                        )
                        db.add(new_speciality)
                    else:
                        # existing_record = next((rec for rec in pop_specialities if rec.site_rec_pop_grp_id == question.incrementid), None)
                        existing_record = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_rec_pop_grp_id == question.incrementid).first()
                        if existing_record:
                            existing_record.specialities_subspecialities_id = speciality.specialities
                            existing_record.question = spec_question_id[0]
                            existing_record.input = question.answer
                            existing_record.updated_by_id = data.updated_by_id

            db.commit()
            return {'response': "Population data updated successfully"}
        finally:
            db.close() 

    def delete_rec_population_grp_specialities(self,site_id,id): 
        db = next(get_db()) 
        try:
            specialities = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == site_id).filter(Rec_Population_grp.specialities_subspecialities_id == id).all()
            if(specialities):
                for speciality in specialities:
                    db.delete(speciality)
                    db.commit()
                return "Speciality deleted Successfully"
        finally:
            db.close()    