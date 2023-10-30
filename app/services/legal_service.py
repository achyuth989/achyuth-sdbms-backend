from app.model.legal import Legal
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from fastapi import HTTPException, status
import bcrypt
from fastapi.logger import logger
from app.db.database import get_db
from datetime import datetime

class Legal_Service:
    def post_legal_docs(self, add_legal):
        db = next(get_db())
        try:
            existing_legal = db.query(Legal).filter(Legal.site_id == add_legal.site_id).first()
            if existing_legal:
                return {"response": f"legal documents for site_id {add_legal.site_id} already exists"}
    
            for questionary in add_legal.questionaries:
                existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
                if existing_question:
                    questionnaire_id = existing_question.questionnaire_id
                    new_legal = Legal(
                        site_id=add_legal.site_id,
                        question=questionnaire_id,
                        answer=questionary.answer,
                        created_by_id=add_legal.created_by_id,
                        created=datetime.now()
                    )
                    db.add(new_legal)
                    db.commit()
                    db.refresh(new_legal)
            return {"response": "Legal document questionnaire added successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def get_by_site_id(self, site_id):
        db = next(get_db())
        try:
            legal_data = db.query(Legal).filter(Legal.site_id == site_id).all()
            for data in legal_data:
                question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
                answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
                if question_data is not None:
                    data.question_text = question_data.question
                    data.answer_text=answer_data.value
            return legal_data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def get_all_legal_docs(self):
        db = next(get_db())
        try:
            legal_data = db.query(Legal).all()
            for data in legal_data:
                question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
                answer_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
                if question_data is not None:
                    data.question_text=question_data.question
                    data.answer_text=answer_data.value
            return legal_data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def update_legal_docs(self, site_id, add_legal):
        db = next(get_db())
        print(add_legal)
        try:
            for questionary in add_legal.questionaries:
                existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
                if existing_question:
                    questionnaire_id = existing_question.questionnaire_id
                    existing_legal = db.query(Legal).filter(Legal.site_id == site_id, Legal.question == questionnaire_id).first()
                    if existing_legal:
                        existing_legal.answer = questionary.answer
                        existing_legal.updated_by_id = add_legal.updated_by_id
                        existing_legal.updated = datetime.now()
                    else:
                        new_it = Legal(
                            site_id=site_id,
                            question=questionnaire_id,
                            answer=questionary.answer,
                            created_by_id=add_legal.updated_by_id,
                            updated_by_id=add_legal.updated_by_id,
                            created=datetime.now(),
                            updated=datetime.now()
                        )
                        db.add(new_it)
            db.commit()
            return {"response": "Legal Documents updated successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
