from app.model.it import It
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from fastapi import HTTPException, status
import bcrypt
from fastapi.logger import logger
from app.db.database import get_db
from datetime import datetime

class It_Service:
    def post_it_and_system_infra(self, add_it):
        db = next(get_db())
        print(add_it)
        try:
            existing_it = db.query(It).filter(It.site_id == add_it.site_id).first()
            if existing_it:
                return {"response": f"IT infra questionnaire for site_id {add_it.site_id} already exists"}
    
            for questionary in add_it.questionaries:
                existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
                if existing_question:
                    questionnaire_id = existing_question.questionnaire_id
                    new_it = It(
                        site_id=add_it.site_id,
                        question=questionnaire_id,
                        answer=questionary.answer,
                        input=questionary.input,
                        created_by_id=add_it.created_by_id,
                        created=datetime.now()
                    )
                    db.add(new_it)
                    db.commit()
                    db.refresh(new_it)
            return {"response": "IT infra questionnaire added successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()



    #def update_it_and_system_infra(self, site_id, add_it):
    #    db = next(get_db())
    #    print(add_it)
    #    try:
    #        for questionary in add_it.questionaries:
    #            existing_it = db.query(It).filter(It.site_id == site_id, It.question == questionary.question).first()
    #            if existing_it:
    #                existing_it.answer = questionary.answer
    #                existing_it.updated_by_id = add_it.updated_by_id
    #                existing_it.updated = datetime.now()
    #        db.commit()
    #        return {"response": "IT infra questionnaire updated successfully"}
    #    except Exception as e:
    #        db.rollback()
    #        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #    finally:
    #        db.close()

    # def get_by_site_id(self, site_id):
    #     db = next(get_db())
    #     try:
    #         it_data = db.query(It).filter(It.site_id == site_id).all()
    #         for data in it_data:
    #             question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
    #             answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
    #             if question_data is not None:
    #                 data.question_text = question_data.question
    #                 data.answer_text=answer_data.value
    #         return it_data
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #     finally:
    #         db.close()
    
    
    def get_by_site_id(self, site_id):
        db = next(get_db())
        try:
            it_data = db.query(It).filter(It.site_id == site_id).all()
            for data in it_data:
                question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
                if question_data is not None:
                    data.question_text = question_data.question
                answer_ids = list(map(int, data.answer))
                answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id.in_(answer_ids)).all()
                data.answer_text = ', '.join(answer.value for answer in answer_data)       
            return it_data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    # def get_all_it_and_system_infra(self):
    #     db = next(get_db())
    #     try:
    #         it_data = db.query(It).all()
    #         for data in it_data:
    #             question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
    #             answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
    #             if question_data is not None:
    #                 data.question_text=question_data.question
    #                 data.answer_text=answer_data.value
    #         return it_data
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #     finally:
    #         db.close()
    
    def get_all_it_and_system_infra(self):
        db = next(get_db())
        try:
            it_data = db.query(It).all()
            for data in it_data:
                question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
                # answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
                if question_data is not None:
                    data.question_text=question_data.question
                answer_ids = list(map(int, data.answer))
                # Query the Miscellaneous table with the converted answer_ids
                answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id.in_(answer_ids)).all()
                # Assuming answer_data is a list, you can concatenate the values as needed
                data.answer_text = ', '.join(answer.value for answer in answer_data)        
            return it_data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()


    def update_it_and_system_infra(self, site_id, add_it):
        db = next(get_db())
        print(add_it)
        try:
            for questionary in add_it.questionaries:
                existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
                if existing_question:
                    questionnaire_id = existing_question.questionnaire_id
                    existing_it = db.query(It).filter(It.site_id == site_id, It.question == questionnaire_id).first()
                    if existing_it:
                        existing_it.answer = questionary.answer
                        existing_it.input = questionary.input
                        existing_it.updated_by_id = add_it.updated_by_id
                        existing_it.updated = datetime.now()
                    else:
                        new_it = It(
                            site_id=site_id,
                            question=questionnaire_id,
                            answer=questionary.answer,
                            input=questionary.input,
                            created_by_id=add_it.updated_by_id,
                            updated_by_id=add_it.updated_by_id,
                            created=datetime.now(),
                            updated=datetime.now()
                        )
                        db.add(new_it)
            db.commit()
            return {"response": "IT infra questionnaire updated successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
    

    #def update_it_and_system_infra(self, site_id, add_it):
    #    db = next(get_db())
    #    print(add_it)
    #    try:
    #        for questionary in add_it.questionaries:
    #            existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
    #            if existing_question:
    #                questionnaire_id = existing_question.questionnaire_id
    #                existing_it = db.query(It).filter(It.site_id == site_id, It.question == questionnaire_id).first()
    #                if existing_it:
    #                    existing_it.answer = questionary.answer
    #                    existing_it.input = questionary.input
    #                    existing_it.updated_by_id = add_it.updated_by_id
    #                    existing_it.updated = datetime.now()
    #        db.commit()
    #        return {"response": "IT infra questionnaire updated successfully"}
    #    except Exception as e:
    #        db.rollback()
    #        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #    finally:
    #        db.close()
