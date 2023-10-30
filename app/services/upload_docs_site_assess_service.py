from app.model.user import User
from app.model.questionnaire import Questionnaire
from app.model.miscellaneous import Miscellaneous
from app.model.site_assess_registration import Site_Assess_Registration
from app.model.study_phases import StudyPhases
from app.model.service_category import Service_Category
from app.model.site_services import SiteServices
from app.model.upload_documents import Upload_Documents
from app.model.site_asmt_infrastructure import SiteAsmtInfrastructure
from app.model.legal import Legal
from app.model.document_status import Document_Status


from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc,not_,asc

class Upload_Docs_Site_Assess_Service:
    def get_site_assess_docs(self,id):
        db = next(get_db())
        try:
            site_assessment_documents = {}
            yes_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == "yes").first()

            # infra_list = db.query(SiteAsmtInfrastructure.site_asmt_infra_equal_id,SiteAsmtInfrastructure.site_id,Questionnaire.questionnaire_id,Questionnaire.question)\
            # .join(Questionnaire,Questionnaire.questionnaire_id == SiteAsmtInfrastructure.question)\
            # .filter(SiteAsmtInfrastructure.answer == yes_id[0])\
            # .filter(SiteAsmtInfrastructure.site_id == id).all()

            entire_list = db.query(Legal.site_asmt_doc_id,Legal.site_id,Questionnaire.questionnaire_id,Questionnaire.question)\
            .join(Questionnaire,Questionnaire.questionnaire_id == Legal.question)\
            .filter(Legal.answer == yes_id[0])\
            .filter(Legal.site_id == id).all()
            target_questions = [
                "Sanitary licence or operation notice?",
                "Sanitary responsible notice?",
                "Ethics committee agreement?",
                "Investigation committee agreement?",
                "Ambulance service or agreement?"
            ]
            legal_documents = [obj for obj in entire_list if obj['question'] in target_questions]
            general_documents = [obj for obj in entire_list if obj['question'] not in target_questions]
            # experience_in_studies = db.query(Site_Assess_Registration.experience_in_studies).filter(Site_Assess_Registration.experience_in_studies != " ").filter(Site_Assess_Registration.site_id == id).first()
            # if(experience_in_studies):
            #     list_exp = experience_in_studies[0].split(',')
            #     ids = [eval(i) for i in list_exp]

            #     phase_list=[]
            #     for phase_id in ids:
            #         study_phases = db.query(StudyPhases.phases_type,StudyPhases.study_phase_id).filter(StudyPhases.study_phase_id == phase_id).first()
            #         phase_list.append(study_phases)
            #     if phase_list:
            #         site_assessment_documents["Experience_in_Studies"] = phase_list


            # services = db.query(Site_Assess_Registration.services,Service_Category.service_category_id,Service_Category.description)\
            # .join(Service_Category,Service_Category.service_category_id == Site_Assess_Registration.category_id)\
            # .filter(Site_Assess_Registration.site_id == id).all() 

            # service_list={}
            # for service in services:
            #     service_array = service.services.split(',')
            #     service_ids = [eval(i) for i in service_array] 
            #     for service_id in service_ids:
            #         category_service = db.query(SiteServices.service_category_description,SiteServices.site_ser_id).filter(SiteServices.site_ser_id == service_id).first()
            #         service_list.setdefault(service.description, []).append(category_service)
                    # service_list[service.description] = category_service
            # service_list = []
            # for service in services:
            #     service_array = service.services.split(',')
            #     service_ids = [eval(i) for i in service_array] 
            #     for service_id in service_ids:
            #         category_service = db.query(SiteServices.service_category_description, SiteServices.site_ser_id).filter(SiteServices.site_ser_id == service_id).first()
            #         service_object = {
            #         "service_category_description": category_service.service_category_description,
            #         "site_ser_id": category_service.site_ser_id,
            #         "category_name": service.description
            #         }
            #         service_list.append(service_object)        

            # site_assessment_documents['Outsourced_Services'] = service_list
            # site_assessment_documents['Infrastructure_Equipment'] = infra_list
            site_assessment_documents['General'] = general_documents
            site_assessment_documents['Legal']=legal_documents
             
            return site_assessment_documents
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def post_site_assess_docs(self,data):
        db = next(get_db())
        existing_site = db.query(Upload_Documents).filter(Upload_Documents.site_id == data.site_id).filter(Upload_Documents.screen_type_name == "Site Assessment").first()
        if(existing_site):
            return{"response":"Assessment Documents are already added to this Site"}
        else:    
            try:
                # screen_name = "Site Assessment"
                # studies_label_name = "Experience in Studies"
                # experience_in_studies_list=[]
            
                # for document in data.experience_in_studies:
                #     attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == document.document_attached).first()
                #     new_experience_in_studies = Upload_Documents(
                #         site_id = data.site_id,
                #         screen_type_name = screen_name,
                #         screen_label_name = studies_label_name,
                #         document_name = document.document_name,
                #         document_attached = attached_id[0],
                #         version = document.version,
                #         status = document.status,
                #         remarks = document.remarks,
                #         attachment = document.attachment,
                #         created_by_id = data.created_by_id
                #     )
                #     experience_in_studies_list.append(new_experience_in_studies)
                # db.add_all(experience_in_studies_list)
                # db.commit()
                # for study in experience_in_studies_list:
                #     db.refresh(study)

                # service_label_name = "Outsourced Services"
                # outsourced_services_list=[]
            
                # for document in data.outsourced_services:
                #     attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == document.document_attached).first()
                #     new_outsourced_service = Upload_Documents(
                #         site_id = data.site_id,
                #         screen_type_name = screen_name,
                #         screen_label_name = service_label_name,
                #         document_name = document.document_name,
                #         document_attached = attached_id[0],
                #         version = document.version,
                #         status = document.status,
                #         remarks = document.remarks,
                #         attachment = document.attachment,
                #         created_by_id = data.created_by_id
                #     )
                #     outsourced_services_list.append(new_outsourced_service)
                # db.add_all(outsourced_services_list)
                # db.commit()
                # for service in outsourced_services_list:
                #     db.refresh(service)

                # infra_equipment_label_name = "Infrastructure & Equipment"
                # infra_equipment_list=[]
            
                # for document in data.infra_equipment:
                #     attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == document.document_attached).first()
                #     new_infra_equipment = Upload_Documents(
                #         site_id = data.site_id,
                #         screen_type_name = screen_name,
                #         screen_label_name = infra_equipment_label_name,
                #         document_name = document.document_name,
                #         document_attached = attached_id[0],
                #         version = document.version,
                #         status = document.status,
                #         remarks = document.remarks,
                #         attachment = document.attachment,
                #         created_by_id = data.created_by_id
                #     )
                #     infra_equipment_list.append(new_infra_equipment)
                # db.add_all(infra_equipment_list)
                # db.commit()
                # for equipment in infra_equipment_list:
                #     db.refresh(equipment)   


                general_label_name = "General"
                general_list=[]
            
                for document in data.general:
                    attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == document.document_attached).first()
                    new_general = Upload_Documents(
                        site_id = data.site_id,
                        screen_type_name = screen_name,
                        screen_label_name = general_label_name,
                        document_name = document.document_name,
                        document_attached = attached_id[0],
                        version = document.version,
                        status = document.status,
                        remarks = document.remarks,
                        attachment = document.attachment,
                        created_by_id = data.created_by_id
                    )
                    general_list.append(new_general)
                db.add_all(general_list)
                db.commit()
                for general in general_list:
                    db.refresh(general)

                legal_label_name = "Legal"
                legal_list=[]
            
                for document in data.legal:
                    attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == document.document_attached).first()
                    new_legal = Upload_Documents(
                        site_id = data.site_id,
                        screen_type_name = screen_name,
                        screen_label_name = legal_label_name,
                        document_name = document.document_name,
                        document_attached = attached_id[0],
                        version = document.version,
                        status = document.status,
                        remarks = document.remarks,
                        attachment = document.attachment,
                        created_by_id = data.created_by_id
                    )
                    legal_list.append(new_legal)
                db.add_all(legal_list)
                db.commit()
                for legal in legal_list:
                    db.refresh(legal)    
                return{"response":"Site Assessment Documents Uploaded Successfully"}  
    
            finally:
                db.close()

    def get_uploaded_site_assess_docs(self,id):
        db = next(get_db())
        try:
            # experience_in_studies = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == id)\
            # .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            # .filter(Upload_Documents.screen_label_name == "Experience in Studies").all()

            # outsourced_services = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == id)\
            # .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            # .filter(Upload_Documents.screen_label_name == "Outsourced Services").all()

            # infra_equipment = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == id)\
            # .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            # .filter(Upload_Documents.screen_label_name == "Infrastructure & Equipment").all()
            site_assessment_documents ={}
            general = db.query(Upload_Documents.site_id,Upload_Documents.screen_label_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Upload_Documents.document_attached,Miscellaneous.value,Document_Status.document_status_description)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            .filter(Upload_Documents.site_id == id)\
            .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            .filter(Upload_Documents.screen_label_name == "General").order_by(desc(Upload_Documents.created)).all()

            general_document_dict = {}
            for result in general:
                document_name = result.document_name
                if document_name not in general_document_dict:
                    general_document_dict[document_name] = {
                        "site_id": result.site_id,
                        # "cr_id": result.cr_code,
                        "screen_label_name": result.screen_label_name,
                        "document_name": document_name,
                        "value": result.value,
                        # "status": result.status,
                        "remarks": result.remarks,
                        "versions": []
                    }
                general_document_dict[document_name]["versions"].append({
                    "upload_document_id": result.upload_document_id,
                    "version": result.version,
                    "attachment": result.attachment,
                    "status": result.status,
                })

            # Convert the dictionary values to a list
            grouped_results = list(general_document_dict.values())

            if grouped_results:
                site_assessment_documents["general"] = grouped_results   

            legal = db.query(Upload_Documents.site_id,Upload_Documents.screen_label_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Upload_Documents.document_attached,Miscellaneous.value,Document_Status.document_status_description)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            .filter(Upload_Documents.site_id == id)\
            .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            .filter(Upload_Documents.screen_label_name == "Legal").order_by(desc(Upload_Documents.created)).all()
             
            legal_document_dict = {}
            for result in legal:
                document_name = result.document_name
                if document_name not in legal_document_dict:
                    legal_document_dict[document_name] = {
                        "site_id": result.site_id,
                        # "cr_id": result.cr_code,
                        "screen_label_name": result.screen_label_name,
                        "document_name": document_name,
                        "value": result.value,
                        # "status": result.status,
                        "remarks": result.remarks,
                        "versions": []
                    }
                legal_document_dict[document_name]["versions"].append({
                    "upload_document_id": result.upload_document_id,
                    "version": result.version,
                    "attachment": result.attachment,
                    "status": result.status,
                })

            # Convert the dictionary values to a list
            legal_results = list(legal_document_dict.values())

            if legal_results:
                site_assessment_documents["Legal"] = legal_results
            # site_assessment_documents['experience_in_studies'] = experience_in_studies
            # site_assessment_documents['outsourced_services'] = outsourced_services
            # site_assessment_documents['infrastructure_equipment'] = infra_equipment
            # site_assessment_documents['general'] = general
            # site_assessment_documents['legal'] = legal

            return site_assessment_documents
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()  

      
    def update_uploaded_site_assess_docs(self, data):
        db = next(get_db())
        try:
            # existing_documents = db.query(Upload_Documents)\
            #     .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            #     .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            #     .filter(Upload_Documents.site_id == id)\
            #     .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            #     .filter(Upload_Documents.screen_label_name == "Experience in Studies").all()

            # existing_document_names = [doc.document_name for doc in existing_documents]

            # for experience in data.experience_in_studies:
            #     if experience.document_name in existing_document_names:
            #         document = next(doc for doc in existing_documents if doc.document_name == experience.document_name)
            #         attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == experience.document_attached).first()
            #         document.document_attached = attached_id[0]
            #         document.version = experience.version
            #         document.status = experience.status
            #         document.remarks = experience.remarks
            #         document.attachment = experience.attachment 
            #         document.updated_by_id = data.updated_by_id
            #     else:
            #         new_attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == experience.document_attached).first()

            #         new_document = Upload_Documents(
            #             site_id = id,
            #             document_name=experience.document_name,
            #             screen_type_name = "Site Assessment",
            #             screen_label_name = "Experience in Studies",
            #             document_attached = new_attached_id[0],
            #             version = experience.version,
            #             status = experience.status,
            #             remarks = experience.remarks,
            #             attachment = experience.attachment,
            #             created_by_id = data.updated_by_id
            #         )
            #         db.add(new_document)
            #         existing_documents.append(new_document)

            # db.commit() 

            # outsourced_services = db.query(Upload_Documents)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == id)\
            # .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            # .filter(Upload_Documents.screen_label_name == "Outsourced Services").all() 

            # services_document_names = [doc.document_name for doc in outsourced_services]

            # for service in data.outsourced_services:
            #     if service.document_name in services_document_names:
            #         service_document = next(doc for doc in outsourced_services if doc.document_name == service.document_name)
            #         service_attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == service.document_attached).first()
            #         service_document.document_attached = service_attached_id[0]
            #         service_document.version = service.version
            #         service_document.status = service.status
            #         service_document.remarks = service.remarks
            #         service_document.attachment = service.attachment 
            #         service_document.updated_by_id = data.updated_by_id
            #     else:
            #         new_service_attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == service.document_attached).first()

            #         new_service_document = Upload_Documents(
            #             site_id = id,
            #             document_name=service.document_name,
            #             screen_type_name = "Site Assessment",
            #             screen_label_name = "Outsourced Services",
            #             document_attached = new_service_attached_id[0],
            #             version = service.version,
            #             status = service.status,
            #             remarks = service.remarks,
            #             attachment = service.attachment,
            #             created_by_id = data.updated_by_id
            #         )
            #         db.add(new_service_document)
            #         outsourced_services.append(new_service_document)

            # db.commit() 

            # infra_equipment = db.query(Upload_Documents)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == id)\
            # .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            # .filter(Upload_Documents.screen_label_name == "Infrastructure & Equipment").all()

            # infra_document_names = [doc.document_name for doc in infra_equipment]

            # for infra in data.infra_equipment:
            #     if infra.document_name in infra_document_names:
            #         infra_document = next(doc for doc in infra_equipment if doc.document_name == infra.document_name)
            #         infra_attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == infra.document_attached).first()
            #         infra_document.document_attached = infra_attached_id[0]
            #         infra_document.version = infra.version
            #         infra_document.status = infra.status
            #         infra_document.remarks = infra.remarks
            #         infra_document.attachment = infra.attachment 
            #         infra_document.updated_by_id = data.updated_by_id
            #     else:
            #         new_infra_attached_id = db.query(Miscellaneous.miscellaneous_id).filter(Miscellaneous.value == infra.document_attached).first()

            #         new_infra_document = Upload_Documents(
            #             site_id = id,
            #             document_name=infra.document_name,
            #             screen_type_name = "Site Assessment",
            #             screen_label_name = "Infrastructure & Equipment",
            #             document_attached = new_infra_attached_id[0],
            #             version = infra.version,
            #             status = infra.status,
            #             remarks = infra.remarks,
            #             attachment = infra.attachment,
            #             created_by_id = data.updated_by_id
            #         )
            #         db.add(new_infra_document)
            #         infra_equipment.append(new_infra_document)

            # db.commit() 


            
            
            # general_documents = db.query(Upload_Documents)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == id)\
            # .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            # .filter(Upload_Documents.screen_label_name == "General").all()

            general_document_list = []

            for doc in data.general:
                attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == doc.document_attached).first()
                for version in doc.versions:
                    existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == version.upload_document_id).first() 
                    if existed_id:
                        
                        existed_id.document_attached = attached_id.miscellaneous_id,
                        existed_id.version = version.version,
                        existed_id.status = version.status,
                        existed_id.remarks = doc.remarks,
                        existed_id.attachment = version.attachment,
                        existed_id.updated_by_id = data.updated_by_id
                        db.commit()     
                    else:

                        new_general_document = Upload_Documents(
                            site_id = data.site_id,
                            document_name=doc.document_name,
                            screen_type_name = "Site Assessment",
                            screen_label_name = "General",
                            document_attached = attached_id.miscellaneous_id,
                            version = version.version,
                            status = version.status,
                            remarks = doc.remarks,
                            attachment = version.attachment,
                            created_by_id = data.updated_by_id
                        )
                        general_document_list.append(new_general_document)
            db.add_all(general_document_list)
            db.commit()

            # legal_documents = db.query(Upload_Documents)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == id)\
            # .filter(Upload_Documents.screen_type_name == "Site Assessment")\
            # .filter(Upload_Documents.screen_label_name == "Legal").all()

            legal_document_list = []

            for doc in data.legal:
                attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == doc.document_attached).first()
                for version in doc.versions:
                    existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == version.upload_document_id).first() 
                    if existed_id:
                        
                        existed_id.document_attached = attached_id.miscellaneous_id,
                        existed_id.version = version.version,
                        existed_id.status = version.status,
                        existed_id.remarks = doc.remarks,
                        existed_id.attachment = version.attachment,
                        existed_id.updated_by_id = data.updated_by_id
                        db.commit()     
                    else:

                        new_legal_document = Upload_Documents(
                            site_id = data.site_id,
                            document_name=doc.document_name,
                            screen_type_name = "Site Assessment",
                            screen_label_name = "Legal",
                            document_attached = attached_id.miscellaneous_id,
                            version = version.version,
                            status = version.status,
                            remarks = doc.remarks,
                            attachment = version.attachment,
                            created_by_id = data.updated_by_id
                        )
                        legal_document_list.append(new_legal_document)
                db.add_all(legal_document_list)
                db.commit()

            return "Site Assessment Documents Updated Successfully"
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
        