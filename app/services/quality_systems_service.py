from app.model.quality_systems import QualitySystems
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from fastapi import HTTPException, status
import bcrypt
from fastapi.logger import logger
from app.db.database import get_db
from sqlalchemy import and_ , func, or_,Integer,cast
from datetime import datetime

class QualitySystems_Service:
    def post_qualitysystems(self, add_qualitysystems):
        db = next(get_db())
        print(add_qualitysystems)
        try:
            existing_quality = db.query(QualitySystems).filter(QualitySystems.site_id == add_qualitysystems.site_id).first()
            if existing_quality:
                return {"response": f"quality systems for site_id {add_qualitysystems.site_id} already exists"}

            for questionary in add_qualitysystems.questionaries:
                existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
                if existing_question:
                    questionnaire_id = existing_question.questionnaire_id
                    new_qualitysystems = QualitySystems(
                        site_id=add_qualitysystems.site_id,
                        question=questionnaire_id,  
                        input=questionary.input,
                        created_by_id=add_qualitysystems.created_by_id,
                        created=datetime.now()
                    )
                    db.add(new_qualitysystems)
                    db.commit()
                    db.refresh(new_qualitysystems)
            return {"response": "Quality systems added successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()


    def get_by_site_id(self, site_id):
        db = next(get_db())
        try:
            quality_sytems_data = db.query(QualitySystems).filter(QualitySystems.site_id == site_id).filter().all()
            for data in quality_sytems_data:
                question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
                question_data_answ = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
                if question_data is not None:
                    data.question_text = question_data.question
                if question_data_answ:    
                    data.answer_text = question_data_answ.value
            return quality_sytems_data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    # def get_by_site_id(self, site_id):
    #     db = next(get_db())
    #     try:
    #         quality_sytems_data = db.query(QualitySystems).filter(QualitySystems.site_id == site_id).all()
    #         for data in quality_sytems_data:
    #             question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
    #             if question_data is not None:
    #                 data.question_text = question_data.question
    #         return quality_sytems_data
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #     finally:
    #         db.close()

    def get_qualitysystems(self):
        db = next(get_db())
        try:
            quality_systems_data = db.query(QualitySystems).all()
            for data in quality_systems_data:
                question_data = db.query(Questionnaire).filter(Questionnaire.questionnaire_id == data.question).first()
                question_data_answ = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.answer).first()
                if question_data is not None:
                    data.question_text=question_data.question
                if question_data_answ:    
                    data.answer_text = question_data_answ.value
            return quality_systems_data
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    #def update_qualitysystems(self, site_id, add_qualitysystems):
    #    db = next(get_db())
    #    print(add_qualitysystems)
    #    try:
    #        for questionary in add_qualitysystems.questionaries:
    #            existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
    #            if existing_question:
    #                questionnaire_id = existing_question.questionnaire_id
    #                existing_qualitysystems = db.query(QualitySystems).filter(QualitySystems.site_id == site_id, QualitySystems.question == questionnaire_id).first()
    #                if existing_qualitysystems:
    #                    existing_qualitysystems.input = questionary.input
    #                    existing_qualitysystems.updated_by_id = add_qualitysystems.updated_by_id
    #                    existing_qualitysystems.updated = datetime.now()
    #        db.commit()
    #        return {"response": "Quality Systems updated successfully"}
    #    except Exception as e:
    #        db.rollback()
    #        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #    finally:
    #        db.close()

    def update_qualitysystems(self, site_id, add_qualitysystems):
        db = next(get_db())
        print(add_qualitysystems)
        try:
            for questionary in add_qualitysystems.questionaries:
                existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
                if existing_question:
                    questionnaire_id = existing_question.questionnaire_id
                    existing_qualitysystems = db.query(QualitySystems).filter(QualitySystems.site_id == site_id, QualitySystems.question == questionnaire_id).first()
                    if questionary.answer :
                        miscellaneous_val = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == questionary.answer.lower()).first()
                        print(miscellaneous_val)
                    if existing_qualitysystems:
                        if existing_question.type == "number" :
                            existing_qualitysystems.answer = miscellaneous_val.miscellaneous_id
                            existing_qualitysystems.updated_by_id = add_qualitysystems.updated_by_id
                            existing_qualitysystems.updated = datetime.now()              
                            db.commit()
                        else:
                            existing_qualitysystems.input = questionary.input
                            existing_qualitysystems.updated_by_id = add_qualitysystems.updated_by_id
                            existing_qualitysystems.updated = datetime.now()
                            db.commit()

                    else:
                        if existing_question.type == "number" :
                            new_qualitysystems = QualitySystems(
                                site_id=site_id,
                                question=questionnaire_id,
                                answer=miscellaneous_val.miscellaneous_id,
                                created_by_id=add_qualitysystems.updated_by_id,
                                created=datetime.now(),
                                updated_by_id=add_qualitysystems.updated_by_id,
                                updated=datetime.now()
                            )
                            db.add(new_qualitysystems)
                            db.commit()
                        else:
                            new_qualitysystems = QualitySystems(
                                site_id=site_id,
                                question=questionnaire_id,
                                input=questionary.input,
                                created_by_id=add_qualitysystems.updated_by_id,
                                created=datetime.now(),
                                updated_by_id=add_qualitysystems.updated_by_id,
                                updated=datetime.now()
                            )
                            db.add(new_qualitysystems)
                            db.commit()
            return {"response": "Quality Systems updated successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()




        # db = next(get_db())
        # print(add_qualitysystems)
        # try:
        #     for questionary in add_qualitysystems.questionaries:
        #         existing_question = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
        #         if existing_question:
        #             questionnaire_id = existing_question.questionnaire_id
        #             existing_qualitysystems = db.query(QualitySystems).filter(QualitySystems.site_id == site_id, QualitySystems.question == questionnaire_id).first()
        #             if existing_qualitysystems:
        #                 existing_qualitysystems.input = questionary.input
        #                 existing_qualitysystems.updated_by_id = add_qualitysystems.updated_by_id
        #                 existing_qualitysystems.updated = datetime.now()
        #             else:
        #                 new_qualitysystems = QualitySystems(
        #                     site_id=site_id,
        #                     question=questionnaire_id,
        #                     input=questionary.input,
        #                     created_by_id=add_qualitysystems.updated_by_id,
        #                     created=datetime.now(),
        #                     updated_by_id=add_qualitysystems.updated_by_id,
        #                     updated=datetime.now()
        #                 )
        #                 db.add(new_qualitysystems)
        #     db.commit()
        #     return {"response": "Quality Systems updated successfully"}
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        # finally:
        #     db.close()
