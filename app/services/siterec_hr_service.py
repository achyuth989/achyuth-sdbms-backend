from app.db.database import get_db
from app.model.site_rec_hr  import Siterec_hr
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from app.model.specialities_subspecialities import Specalitiess
from app.model.speciality_subspeciality import SpecialitySubspeciality
from app.model.speciality import Speciality
from sqlalchemy.sql import func
from app.model.cr_roles import Cr_Roles
from app.model.site import Site
from app.schemas.siterec_hr_schema import Sitehr
from fastapi import HTTPException,status
from datetime import datetime



class Site_rec_hr:
    def post_siterec_hr(self,records):
        db = next(get_db())
        site_assment = db.query(Siterec_hr).filter(Siterec_hr.site_id == records.site_id).first()
        if site_assment:
            raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "Site id with data  already exist.")
        else:
            try:
                for data in records.questionary:
                    actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == data.question).first()
                    question_id = actual_question_record.questionnaire_id
                    if data.type== "yes":
                        # for answer in data.answer:
                        answers = data.answer[0]
                        answer_id = int(answers)

                        
                        new_hr = Siterec_hr(
                            site_id=records.site_id,
                            question = question_id,
                            answer = answer_id,
                            # input = input_filed,
                            created_by_id = records.created_by_id
                        )
                        db.add(new_hr)
                        db.commit()
                        db.refresh(new_hr)

                        response = "added to db"
                        
                    elif data.type == "staff":
                        # all_answers=[]
                        for staff_input in data.answer:
                            answer = int(staff_input)
                            new_hr = Siterec_hr(
                                site_id=records.site_id,
                                question = question_id,
                                input = answer,
                                created_by_id = records.created_by_id
                            )
                            db.add(new_hr)
                            db.commit()
                            db.refresh(new_hr)
                            response= "added nurses"
                        
                for data in records.specialities:
                    actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == data.question).first()
                    question_id = actual_question_record.questionnaire_id
                    new_hr_spec = Siterec_hr(
                        site_id=records.site_id,
                        question = question_id,
                        speciality_subspeciality_id=data.speciality_subspeciality_id,
                        count=data.count,
                        created_by_id=records.created_by_id
                    ) 
                    db.add(new_hr_spec)
                    db.commit()
                    db.refresh(new_hr_spec)
                    response= "added specialities"

                for data in records.contactlist:
                    Miscellaneous_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == data.salutation).scalar()

                    new_hr = Siterec_hr(
                        site_id=records.site_id,
                        role = data.role,
                        salutation = Miscellaneous_id,
                        first_name = data.first_name,
                        last_name = data.last_name,
                        stand = data.stand,
                        contact_phone = data.contact_phone,
                        contact_email = data.contact_email,
                        created_by_id = records.created_by_id
                    )
                    db.add(new_hr)
                    db.commit()
                    db.refresh(new_hr)
                    response= "added contalist"

                return "all details added succesfully"
            finally:
                db.close()




    def get_sitehr_by_id(self,site_id):
        db = next(get_db())           
        try:
        
            site_hr_details =  db.query(Siterec_hr).filter(Siterec_hr.site_id == site_id).all()
            if site_hr_details:
                questions_list =[]
                specialities_list = []
                contact_list =[]
                for details in site_hr_details:
                    
                    # specialities_list =[]
                    # contact_list =[]
                    # if details.speciality_subspeciality_id is None and details.count is None and details.input is None:
                    if details.answer is not None:

                        question_id = details.question
                        question_record = db.query(Questionnaire).filter(Questionnaire.questionnaire_id== question_id).first()
                        final_question = question_record.question
                        # details.question = final_question
                        answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==details.answer).first()
                        final_answer = answer_record.value
                        # details.final_answer= final_answer
                        

                        q_a_pair = {
                            "site_id":details.site_id,
                            "question_id":question_id,
                            "answer_id":details.answer,
                            "question_record":final_question,
                            "answer_record":final_answer,
                            "site_rec_hr_id":details.site_rec_hr_id
                        }
                        
                        questions_list.append(q_a_pair)
                    elif details.input is not None:

                        question_id = details.question
                        question_record = db.query(Questionnaire).filter(Questionnaire.questionnaire_id== question_id).first()
                        final_question = question_record.question
                        # details.question = final_question

                        q_a_pair = {
                            "site_id":details.site_id,
                            "question_id":question_id,
                            "question_record":final_question,
                            "input_answer":details.input,
                            "site_rec_hr_id":details.site_rec_hr_id
                        }
                        questions_list.append(q_a_pair)


                    
                    elif details.speciality_subspeciality_id is not None:
                        question_id = details.question
                        question_record = db.query(Questionnaire).filter(Questionnaire.questionnaire_id== question_id).first()
                        final_question = question_record.question
                        details.question = final_question
                        answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==details.answer).first()
                        


                        speciality_subspec_id_record = db.query(Specalitiess).filter(Specalitiess.specialities_subspecialities_id==details.speciality_subspeciality_id).first()
                        
                        speciality_subspec_id = speciality_subspec_id_record.spec_sub_id
                        subspeciality_record = db.query(SpecialitySubspeciality).filter(SpecialitySubspeciality.id==speciality_subspec_id).first()
                        
                        subspeciality_answer = subspeciality_record.subspeciality
                      
                        speciality_id1 = subspeciality_record.speciality_id

                        specality_record = db.query(Speciality).filter(Speciality.id == speciality_id1).first()
                        specality_answer = specality_record.speciality



                        specialities_pair = {
                            "site_id":details.site_id,
                            "question_id":question_id,
                            "question_record":final_question,
                            "speciality_value": specality_answer,
                            "subspecality_value":subspeciality_answer,
                            "count":details.count,
                            "specialities_subspecialities_id":details.speciality_subspeciality_id,
                            "site_rec_hr_id":details.site_rec_hr_id
                            
                        }

                        specialities_list.append(specialities_pair)

                    
                    elif details.role is not None: 
                        answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==details.salutation).first()                     
                        # salutation = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id ==  Siterec_hr.salutation).first()
                        final_salutation =answer_record.value
                        contacts_pair = {
                            "site_id":details.site_id,
                            "role":details.role,
                            "salutation":final_salutation,
                            "first_name": details.first_name,
                            "last_name":details.last_name,
                            "stand":details.stand,
                            "contact_phone":details.contact_phone,
                            "contact_email":details.contact_email,
                            "site_rec_hr_id":details.site_rec_hr_id
                            
                        }

                        contact_list.append(contacts_pair)
            
                return {"question":questions_list,"specailities":specialities_list,"contactteam":contact_list}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def update_sitehr(self, site_id, records):
        db = next(get_db())
        try:
            response = ""

            for data in records.questionary:
                site_rec_hr_id = data.site_rec_hr_id
                existing_hr = db.query(Siterec_hr).filter(Siterec_hr.site_rec_hr_id == site_rec_hr_id).first()


                actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == data.question).first()
                question_id = actual_question_record.questionnaire_id

                if data.type == "yes":
                    answers = data.answer[0]
                    answer_id = int(answers)

                    if existing_hr:
                        # Update existing answer
                        existing_hr.answer = answer_id
                        existing_hr.updated_by_id = records.updated_by_id
                        response = "Updated record in db"

                    else:
                        # Insert new answer
                        new_hr = Siterec_hr(
                            site_id=site_id,
                            question=question_id,
                            answer=answer_id,
                            updated_by_id=records.updated_by_id,
                            created_by_id=records.updated_by_id,
                            updated=datetime.now()
                        )
                        db.add(new_hr)
                        response = "Inserted new record in db"

                elif data.type == "staff":
                    staff_changes = False
                    for staff_input in data.answer:
                        answer = int(staff_input)


                        if existing_hr:
                            existing_hr.input = answer
                            existing_hr.updated_by_id = records.updated_by_id
                            staff_changes = True
                        else:
                            new_hr_staff = Siterec_hr(
                                site_id=site_id,
                                question=question_id,
                                input=answer,
                                created_by_id=records.updated_by_id,
                            )
                            db.add(new_hr_staff)

                    if staff_changes:
                        response += "Updated nurses in db\n"
                    else:
                        response += "No changes made for nurses\n"

            db.commit()  
            
            for data in records.specialities:
                    speciality_subspeciality_id, count = map(int, data.answer[0].split(','))

                    # Check if the question exists in the database
                    actual_question_record = db.query(Questionnaire).filter(Questionnaire.question == data.question).first()

                    if actual_question_record:
                        # Question exists, get the corresponding question_id
                        question_id = actual_question_record.questionnaire_id

                        # Check if the entry for this speciality already exists in Siterec_hr
                        existing_hr_spec = db.query(Siterec_hr).filter(
                            Siterec_hr.site_id == site_id,
                            Siterec_hr.question == question_id,
                            Siterec_hr.speciality_subspeciality_id == speciality_subspeciality_id
                        ).first()

                        if existing_hr_spec:
                            existing_hr_spec.count = count
                            existing_hr_spec.updated_by_id = records.updated_by_id
                            response += "Updated specialities in db\n"
                        else:
                            # Insert new Siterec_hr record for the speciality
                            new_hr_spec = Siterec_hr(
                                site_id=site_id,
                                question=question_id,
                                speciality_subspeciality_id=speciality_subspeciality_id,
                                count=count,
                                updated_by_id=records.updated_by_id,
                                created_by_id=records.updated_by_id,
                                updated=datetime.now()
                            )
                            db.add(new_hr_spec)
                            response += "Inserted new speciality in db\n"
                    else:
                        # Question does not exist, create a new Questionnaire record first
                        new_question = Questionnaire(
                            question=data.question,
                            created_by_id=records.updated_by_id,
                            updated_by_id=records.updated_by_id,
                            created=datetime.now(),
                            updated=datetime.now()
                        )
                        db.add(new_question)
                        db.commit()

                        # Now get the newly created question_id
                        question_id = new_question.questionnaire_id

                        # Insert new Siterec_hr record for the speciality
                        new_hr_spec = Siterec_hr(
                            site_id=site_id,
                            question=question_id,
                            speciality_subspeciality_id=speciality_subspeciality_id,
                            count=count,
                            updated_by_id=records.updated_by_id,
                            created_by_id=records.updated_by_id,
                            updated=datetime.now()
                        )
                        db.add(new_hr_spec)
                        response += "Inserted new question and speciality in db\n"

            db.commit()

            for data in records.contactlist:
                site_rec_hr_id = data.site_rec_hr_id
                existing_hr_contact = db.query(Siterec_hr).filter(
                    Siterec_hr.site_rec_hr_id == site_rec_hr_id
                ).first()
                Miscellaneous_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == data.salutation).scalar()

                print("Existing HR Contact:", existing_hr_contact)

                if existing_hr_contact:
                    existing_hr_contact.role = data.role
                    existing_hr_contact.contact_email = data.contact_email
                    existing_hr_contact.salutation = Miscellaneous_id
                    existing_hr_contact.first_name = data.first_name
                    existing_hr_contact.last_name = data.last_name
                    existing_hr_contact.stand = data.stand
                    existing_hr_contact.contact_phone = data.contact_phone
                    existing_hr_contact.updated_by_id = records.updated_by_id
                    response = "Updated contactlist in db"
                else:
                    new_hr_contact = Siterec_hr(
                        site_id=site_id,
                        role=data.role,
                        salutation=Miscellaneous_id,
                        first_name=data.first_name,
                        last_name=data.last_name,
                        stand=data.stand,
                        contact_phone=data.contact_phone,
                        contact_email=data.contact_email,
                        created_by_id=records.updated_by_id
                    )
                    db.add(new_hr_contact)

            db.commit()  

            return "All details updated successfully"

        except Exception as e:
            db.rollback()  
            raise e

        finally:
            db.close()



    def get_delete_hrservice(self,id):
        db = next(get_db())
        try:
            Siterechr = db.query(Siterec_hr).filter(Siterec_hr.site_rec_hr_id == id).first()
            if(Siterechr):
                db.delete(Siterechr)
                db.commit()
                return{"successs":"deleted sucessfully"}
            else:
                return{"error":" Siterechr  data is not deleted"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()



       