from app.model.icd import Icd
from app.model.site import Site
from app.db.database import get_db
from app.model.icd_siterecgonization import Siteicd
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from app.schemas.icd_siterecognization_schema import Icdsite,icds
import bcrypt
from sqlalchemy import func,desc,not_,asc,and_,distinct, tuple_
from fastapi import HTTPException,status
from sqlalchemy.orm import aliased
from datetime import datetime







class Site_icd_diseases:
    def get_site(self):
        db = next(get_db())
        try:
            level_4_icd_codes = db.query(Icd).filter(Icd.icd_level == 4).all()
            return level_4_icd_codes 
        finally:
            db.close()

    def post_site_icd(self,data):
        db = next(get_db())
        site_assment = db.query(Siteicd).filter(Siteicd.site_id == data.site_id).first()
        miscellaneous_record = db.query(Miscellaneous).filter(Miscellaneous.value == data.answer).first()

        if site_assment:
            raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "Site id with data  already exist.")
        else:
            try:
                for icds in data.top_icds:
                    new_icds = Siteicd(
                        top_icd_id=icds.top_icd_id,
                        top_diseases_pathologies=icds.top_diseases_pathologies,
                        top_count_of_thread=icds.top_count_of_thread,
                        site_id = data.site_id,
                        question= data.question,
                        answer = miscellaneous_record.miscellaneous_id,
                        created_by_id = data.created_by_id
                    )
                    db.add(new_icds)
                    db.commit()
                    db.refresh(new_icds)
                for orphans in data.orphan_icds:
                    new_orphans =  Siteicd(
                        orphan_icd_id = orphans.orphan_icd_id,
                        orphan_diseases_pathologies = orphans.orphan_diseases_pathologies,
                        orphan_count_of_thread = orphans.orphan_count_of_thread,
                        site_id = data.site_id,
                        question= data.question,
                        answer = miscellaneous_record.miscellaneous_id,
                        created_by_id = data.created_by_id
                    )
                    db.add(new_orphans)
                    db.commit()
                    db.refresh(new_orphans)
                return {"response":"Top  Disease added successfully"}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            finally:
                db.close()

    
    
     
    def  get_site_icd_rec(slef):
        db = next(get_db())
        try:
            siteicdrec = db.query(Siteicd).all()
            all_records= []
            for records  in siteicdrec:
                Icd_record_1 = db.query(Icd).filter(Icd.icd_id == records.top_icd_id).first()
                Icd_record_2 = db.query(Icd).filter(Icd.icd_id == records.orphan_icd_id).first()
                answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == records.answer).first()


                icdrecord1 = Icd_record_1.icd_code if Icd_record_1 else None
                icdrecord2 = Icd_record_2.icd_code if Icd_record_2 else None
                answer = answer_record.value if answer_record else None


                records.top_icd_idrecord1 = icdrecord1
                records.orphan_icd_idrecord2 = icdrecord2
                records.answer1 = answer
                all_records.append(records)
            return all_records
        finally:
             db.close()
             
   
    
   
    def get_site_icd_by_siteid(self, side_id):
        db = next(get_db())
        try:
            icds_rec = db.query(Siteicd.site_rec_icd_id).filter(Siteicd.site_id == side_id).first()
            questions = db.query(
                Siteicd.site_rec_icd_id,
                Siteicd.answer,
                Siteicd.site_id,
                Questionnaire.question,
                Questionnaire.questionnaire_id,
                Miscellaneous.value
            ) \
            .join(Questionnaire, Siteicd.question == Questionnaire.questionnaire_id) \
            .join(Miscellaneous, Siteicd.answer == Miscellaneous.miscellaneous_id) \
            .filter(Siteicd.site_id == side_id) \
            .all()
            unique_questions = {}
            filtered_questions = []
            for question in questions:
                question_tuple = (
                    question.question,
                    question.answer
                )
                if question_tuple not in unique_questions:
                    unique_questions[question_tuple] = question
                    filtered_questions.append(question)

            topicds = db.query(
                Siteicd.site_rec_icd_id,
                Siteicd.site_id,
                Siteicd.top_icd_id,
                Siteicd.top_diseases_pathologies,
                Siteicd.top_count_of_thread,
                Icd.icd_code
            ) \
            .join(Icd, Siteicd.top_icd_id == Icd.icd_id) \
            .filter(Siteicd.site_id == side_id) \
            .order_by(asc(Siteicd.site_rec_icd_id)) \
            .all()

            orphanicds = db.query(
                Siteicd.site_rec_icd_id,
                Siteicd.site_id,
                Siteicd.orphan_icd_id,
                Siteicd.orphan_diseases_pathologies,
                Siteicd.orphan_count_of_thread,
                Icd.icd_code
            ) \
            .join(Icd, Siteicd.orphan_icd_id == Icd.icd_id) \
            .join(Questionnaire, Siteicd.question == Questionnaire.questionnaire_id) \
            .filter(Siteicd.site_id == side_id) \
            .order_by(asc(Siteicd.site_rec_icd_id)) \
            .all()

            unique_orphanicds = set()
            filtered_orphanicds = []
            for orphanicd in orphanicds:
                orphanicd_tuple = (
                    orphanicd.site_rec_icd_id,
                    orphanicd.site_id,
                    orphanicd.orphan_icd_id,
                    orphanicd.orphan_diseases_pathologies,
                    orphanicd.orphan_count_of_thread,
                    orphanicd.icd_code
                )
                if orphanicd_tuple not in unique_orphanicds:
                    unique_orphanicds.add(orphanicd_tuple)
                    filtered_orphanicds.append(orphanicd)

            complete_object = {}
            complete_object['questions'] = filtered_questions
            complete_object['topicds'] = topicds
            complete_object['orphanicds'] = filtered_orphanicds
            return complete_object
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()










    def update_icd(self, id, data):
        print("Received data:", data)
        db = next(get_db())
        try:
            miscellaneous_record = db.query(Miscellaneous).filter(Miscellaneous.value == data.answer).first()
            for icds in data.top_icds:
                existing_icd = db.query(Siteicd).filter(Siteicd.site_rec_icd_id == icds.site_rec_icd_id).first()
                if existing_icd:
                    existing_icd.top_diseases_pathologies = icds.top_diseases_pathologies
                    existing_icd.top_count_of_thread = icds.top_count_of_thread
                    existing_icd.question = data.question
                    existing_icd.answer = miscellaneous_record.miscellaneous_id
                    existing_icd.site_rec_icd_id = icds.site_rec_icd_id
                    existing_icd.site_id = id  
                    existing_icd.updated_by_id = data.updated_by_id
                    existing_icd.updated = datetime.utcnow()
                    db.commit()
            
                else:
                    new_icd = Siteicd(
                        site_id=id,
                        top_icd_id=icds.top_icd_id,
                        top_diseases_pathologies=icds.top_diseases_pathologies,
                        top_count_of_thread=icds.top_count_of_thread,
                        question=data.question,
                        answer=miscellaneous_record.miscellaneous_id,
                        created_by_id=data.updated_by_id,
                    )
                    db.add(new_icd)
                    db.commit()


            for orphans in data.orphan_icds:
                try:
                    orphan_icd_id = int(orphans.orphan_icd_id)
                except ValueError:
                    print(f"Skipping orphan_icd record with invalid orphan_icd_id: {orphans.orphan_icd_id}")
                    continue
                existing_orphan = db.query(Siteicd).filter(Siteicd.site_rec_icd_id == orphans.site_rec_icd_id).first()

                if existing_orphan:
                    # print("Updating existing record with orphan_icd_id:", existing_orphan.orphan_icd_id)
                    existing_orphan.orphan_diseases_pathologies = orphans.orphan_diseases_pathologies
                    existing_orphan.orphan_count_of_thread = orphans.orphan_count_of_thread
                    existing_orphan.question = data.question
                    existing_orphan.answer = miscellaneous_record.miscellaneous_id
                    existing_orphan.site_rec_icd_id = orphans.site_rec_icd_id
                    existing_orphan.updated_by_id = data.updated_by_id
                    existing_orphan.updated = datetime.utcnow()
                    db.commit()

                else:
                    new_orphan = Siteicd(
                        site_id=id,
                        orphan_icd_id=orphans.orphan_icd_id,
                        orphan_diseases_pathologies=orphans.orphan_diseases_pathologies,
                        orphan_count_of_thread=orphans.orphan_count_of_thread,
                        question=data.question,
                        answer=miscellaneous_record.miscellaneous_id,
                        created_by_id=data.updated_by_id,
                    )
                    db.add(new_orphan)
 
            db.commit()
            return {"response": "Site ICDS updated successfully"}
        # except ValueError:
        #     return{"response":"Site ICDS updated successfully"}

        finally:
            db.close()


            
        


    def get_delete_icd(self,id):
        db = next(get_db())
        try:
            Siteicds = db.query(Siteicd).filter(Siteicd.site_rec_icd_id == id).first()
            if(Siteicds):
                db.delete(Siteicds)
                db.commit()
                return{"successs":"deleted sucessfully"}
            else:
                return{"error":" Siteicds  data is not deleted"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()







 