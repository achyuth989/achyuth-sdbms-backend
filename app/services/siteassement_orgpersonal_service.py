from app.db.database import get_db
from app.model.siteassement_orgpersonal import  Orgpersonal
from app.model.questionnaire import Questionnaire
from app.model.site_rec_hr import Siterec_hr
from app.model.miscellaneous import Miscellaneous
from app.schemas.siteassement_orgpersonal_schema import Siteassementorg,Updatesiteassessment
from fastapi import HTTPException,status
from sqlalchemy import func,desc,not_,asc,cast,String
from datetime import datetime



class  Siteassment_org_personal:
    def post_orgpersonal(self,data):
        db = next(get_db())
        site_assment = db.query(Orgpersonal).filter(Orgpersonal.site_id == data.site_id).first()
        if site_assment:
            raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "Site id with data  already exist.")
        else:
            try:
                for question in data.questions:
                    question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()
                    new_question = Orgpersonal(
                        site_id = data.site_id,
                        question = question_id[0],
                        input = question.answer,
                        created_by_id=data.created_by_id
                    )
                    db.add(new_question)
                    db.commit()
                new_organizations = []
                # Corrected filter value for querying organizations
                # salutation = db.query(Orgpersonal).join(Miscellaneous, Orgpersonal.salutation == Miscellaneous.miscellaneous_id).filter(Orgpersonal.site_id == data.site_id).all()
                # salutation = db.query(Orgpersonal).join(Miscellaneous, Orgpersonal.salutation == Miscellaneous.miscellaneous_id).filter(Orgpersonal.site_id == id).all()
                for organizationpersonal in data.organizations:
                    # Miscellaneous_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == organizationpersonal.salutation).scalar()
                    # Miscellaneous_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == organizationpersonal.salutation).first()
                    new_organization = Orgpersonal(
                        site_id = data.site_id,
                        role = organizationpersonal.role,
                        salutation =organizationpersonal.salutation,
                        first_name= organizationpersonal.first_name,
                        last_name = organizationpersonal.last_name,
                        contact_phone = organizationpersonal.contact_phone,
                        contact_email=organizationpersonal.contact_email,
                        created_by_id=data.created_by_id    
                    )
                    new_organizations.append(new_organization)
                    db.add(new_organization)
                    db.commit()
                return{"response":"Orgpersonal added successfully."}
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            finally:
                db.close()
     

    
    def get_orgpersonal_by_id(self,site_id):
        db= next(get_db())
        try:
            orgdetails = db.query(Orgpersonal).filter(Orgpersonal.site_id == site_id).first()

            questions = db.query(Orgpersonal.site_asmt_org_pers_id,Orgpersonal.site_id,Orgpersonal.input,Questionnaire.question,Questionnaire.questionnaire_id)\
            .join(Questionnaire,Orgpersonal.question == Questionnaire.questionnaire_id)\
            .filter(Orgpersonal.site_id == site_id).filter(Orgpersonal.role.is_(None)).all()

            orgdetailss = db.query(Orgpersonal).filter(Orgpersonal.site_id == site_id).filter(Orgpersonal.question.is_(None)).all()
            # .site_asmt_org_pers_id,Orgpersonal.site_id,Orgpersonal.salutation,Orgpersonal.last_name,Orgpersonal.contact_email,Orgpersonal.input,Orgpersonal.role,Orgpersonal.first_name,Orgpersonal.contact_phone,Orgpersonal.question,Orgpersonal.created_by_id,Orgpersonal.updated_by_id,Orgpersonal.created,Orgpersonal.updated,Miscellaneous.miscellaneous_id,Miscellaneous.value)\
            # .filter(Orgpersonal.salutation == Miscellaneous.miscellaneous_id)
            

            # miscellaneous_val = db.query(Orgpersonal,Miscellaneous.value,Miscellaneous.miscellaneous_id).filter(Orgpersonal.salutation == Miscellaneous.miscellaneous_id).first()
            # value = []
            # value.append(miscellaneous_val)
            # value.append(orgdetailss)
            
            def split_objects_into_pairs(objects):
                pairs = [objects[i:i+2] for i in range(0, len(objects), 2)]
                return pairs
            result = split_objects_into_pairs(orgdetailss)

            complete_deatils = {}
            complete_deatils['questions'] = questions
            complete_deatils['orgdetailss'] = orgdetailss
            # complete_deatils['miscellaneous_val'] = miscellaneous_val
            return complete_deatils
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()



    def update_orgpersonal(self,id,data):
        db= next(get_db())
        print(data)
        try:
            questions = db.query(Orgpersonal)\
            .join(Questionnaire,Orgpersonal.question == Questionnaire.questionnaire_id)\
            .filter(Orgpersonal.site_id == id).all()
            

            # count = 0
            for count,question in enumerate(data.questions):
                question_id = db.query(Questionnaire.questionnaire_id).filter(Questionnaire.question == question.question).first()
                if count < len(questions):
                    questions[count].question = question_id[0],
                    questions[count].input = question.answer,
                    questions[count].updated_by_id = data.updated_by_id
                else:
                    new_question = Orgpersonal(
                        site_id=id,
                        question=question_id[0],
                        input=question.answer,
                        updated_by_id=data.updated_by_id,
                        created_by_id = data.updated_by_id,
                        updated=datetime.now()
                    )
                    db.add(new_question)
                # count+=1
            db.commit()
            existing_roles = db.query(Orgpersonal).filter(Orgpersonal.site_id == id).all()
            existing_role_emails = set(role.contact_email for role in existing_roles)
            # Update roles
            # existing_role_count = len(questions)
            # existing_role_ids = set()
            # salutation = db.query(Orgpersonal).join(Miscellaneous,Orgpersonal.salutation == Miscellaneous.miscellaneous_id)\
            #     .filter(Orgpersonal.site_id == id).all()
            # salutation = db.query(Orgpersonal).join(Miscellaneous, Orgpersonal.salutation == Miscellaneous.miscellaneous_id).filter(Orgpersonal.site_id == id).all()
            # miscellaneous_val = db.query(Miscellaneous).filter(Miscellaneous.value == Orgpersonal.salutation).first()
            for role in data.roles: 
                # Miscellaneous_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == role.salutation).scalar()
                # Miscellaneous_id = db.query(Miscellaneous.miscellaneous_id).first(Miscellaneous.value ==role.salutation).first()
                if role.contact_email in existing_role_emails:
                    # existing_role = db.query(Orgpersonal).filter(
                    # Orgpersonal.site_id == id,Orgpersonal.contact_email == role.contact_email).first()
                    existing_role = next((r for r in existing_roles if r.contact_email == role.contact_email), None)
                    # existing_role = next((role for role in existing_roles if role.contact_email == role.contact_email), None)
                    if existing_role:
                        existing_role.role = role.role
                        existing_role.salutation = role.salutation
                        existing_role.first_name = role.first_name
                        existing_role.last_name = role.last_name
                        existing_role.contact_phone = role.contact_phone
                        existing_role.contact_email = role.contact_email
                        existing_role.updated_by_id =data.updated_by_id
                else:
                    new_role = Orgpersonal(
                        site_id=id,
                        role=role.role,
                        salutation=role.salutation,
                        first_name=role.first_name,
                        last_name=role.last_name,
                        contact_phone=role.contact_phone,
                        contact_email=role.contact_email,
                        # updated_by_id=data.updated_by_id,
                        created_by_id=data.updated_by_id,
                        # updated=datetime.now()
                    )
                    db.add(new_role)

            db.commit()             
            return{"response":"orgpersonal data updated successfully"}
            # return questions
        finally:
            db.close()

    def get_delete_orgpersonal(self,id):
        db = next(get_db())
        try:
            orgpersonal = db.query(Orgpersonal).filter(Orgpersonal.site_asmt_org_pers_id == id).first()
            if(orgpersonal):
                db.delete(orgpersonal)
                db.commit()
                return{"successs":"deleted sucessfully"}
            else:
                return{"error":" organization personal  data is not deleted"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
