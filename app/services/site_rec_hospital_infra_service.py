from app.model.site_rec_hospital_infra import SiteRecHospitalInfra
from app.model.miscellaneous import Miscellaneous
from app.model.questionnaire import Questionnaire
from app.model.service_category import Service_Category
from app.model.services import Site_Services
from app.model.site_services import SiteServices
from app.db.database import get_db
from sqlalchemy import and_ , func, or_
from fastapi import HTTPException, status
from typing import List
import json
import json
class Site_Rec_Hospital_Infra:
    def post_sites_rec_hospital_infra(self,hospital_infra):
        db = next(get_db())
        hospital_site_id= db.query(SiteRecHospitalInfra).filter(SiteRecHospitalInfra.site_id == hospital_infra.site_id).all()
        try:
            if hospital_site_id:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Site id already exist.")
            else :
                if hospital_infra.questionary:
                    for questionary in hospital_infra.questionary:
                        question_id = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
                        if questionary.answer :
                            miscellaneous_val = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == questionary.answer.lower()).first()
                        if question_id.type == "number" :
                            new_hosp_infra = SiteRecHospitalInfra(
                                site_id = hospital_infra.site_id,
                                question = question_id.questionnaire_id,
                                input = questionary.inputvalue,
                                created_by_id = hospital_infra.created_by_id
                            )
                            db.add(new_hosp_infra)
                            db.commit()
                        else:
                            new_hospital_infra = SiteRecHospitalInfra(
                                site_id = hospital_infra.site_id,
                                question = question_id.questionnaire_id,
                                answer = miscellaneous_val.miscellaneous_id,
                                created_by_id = hospital_infra.created_by_id
                            )
                            db.add(new_hospital_infra)
                            db.commit()
                if hospital_infra.service:
                    for checked in hospital_infra.service:
                        new_diagnostic = SiteRecHospitalInfra(
                            site_id = hospital_infra.site_id,
                            service_category_id = checked.service_category,
                            services = checked.services,
                            created_by_id = hospital_infra.created_by_id
                        )
                        db.add(new_diagnostic)
                        db.commit()
                if hospital_infra.certifications:
                    new_certifications = SiteRecHospitalInfra(
                        site_id = hospital_infra.site_id,
                        certification_of_central_laboratory_ids = hospital_infra.certifications,
                        input = hospital_infra.others_certifications,
                        created_by_id = hospital_infra.created_by_id
                    )
                    db.add(new_certifications)
                    db.commit()
                if hospital_infra.equipment:
                    new_equipment = SiteRecHospitalInfra(
                        site_id = hospital_infra.site_id,
                        equipment_available_ids = hospital_infra.equipment,
                        created_by_id = hospital_infra.created_by_id
                    )
                    db.add(new_equipment)
                    db.commit()
                return {"success" : "Hospital infra deatils added successfully."}
        finally:
            db.close()
    def get_sites_rec_hospital_infra(self, site_id):
        db = next(get_db())
        try:
            complete_details = {}
            inputdata = db.query(SiteRecHospitalInfra.site_rec_hospital_infra_id,SiteRecHospitalInfra.site_id,SiteRecHospitalInfra.question,SiteRecHospitalInfra.answer,SiteRecHospitalInfra.input, Questionnaire.question)\
                .join(Questionnaire, SiteRecHospitalInfra.question == Questionnaire.questionnaire_id)\
                .filter(SiteRecHospitalInfra.input != " ")\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .all()
            if inputdata:
                complete_details['inputdata'] = inputdata

            questions = db.query(SiteRecHospitalInfra.site_rec_hospital_infra_id,SiteRecHospitalInfra.site_id,SiteRecHospitalInfra.question,SiteRecHospitalInfra.answer,SiteRecHospitalInfra.input, Questionnaire.question,Miscellaneous.value)\
                .join(Questionnaire, SiteRecHospitalInfra.question == Questionnaire.questionnaire_id)\
                .join(Miscellaneous, Miscellaneous.miscellaneous_id == SiteRecHospitalInfra.answer)\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .all()
            if questions:
                complete_details['questions'] = questions

            servics = db.query(SiteRecHospitalInfra.service_category_id, SiteRecHospitalInfra.services)\
                    .filter(SiteRecHospitalInfra.services != "{NULL}")\
                    .filter(SiteRecHospitalInfra.site_id == site_id)\
                    .all()
            if servics:
                services_all_list = []
                for recservics in servics:
                    category_id = recservics.service_category_id
                    categorys = db.query(Service_Category)\
                    .filter(Service_Category.service_category_id == category_id)\
                    .first()
                    service_type_id = recservics.services
                    service_type_ids = ','.join(str(num) for num in service_type_id)
                    services_list = [int(num) for num in service_type_ids.split(",")]
                    obj = {
                        "service_category_id" : categorys.service_category_id,
                        "service_category": categorys.service_category,
                        "category_description" : categorys.description,
                        "services_list" : services_list
                    }
                    services_all_list.append(obj)
                    complete_details['services_all_list'] = services_all_list
                    
            certificates = db.query(SiteRecHospitalInfra.certification_of_central_laboratory_ids,SiteRecHospitalInfra.input)\
                .filter(SiteRecHospitalInfra.certification_of_central_laboratory_ids != "{NULL}")\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .first()
            if certificates:
                # certificate_type_id = certificates[0][0]
                # certificate_list = [int(num) for num in certificate_type_id.split(",")]
                certification_list = list(map(int, certificates[0]))
                complete_details['certificates'] = certification_list
                
            equipment = db.query(SiteRecHospitalInfra.equipment_available_ids)\
                .filter(SiteRecHospitalInfra.equipment_available_ids != "{NULL}")\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .first()
            if equipment:
                # equipment_type_id = equipment[0][0]
                # equipment_list = [int(num) for num in equipment_type_id.split(",")]
                equipment_list = list(map(int, equipment[0]))
                complete_details['equipment'] = equipment_list
            
                others_certifications = db.query(SiteRecHospitalInfra.input)\
                .filter(SiteRecHospitalInfra.certification_of_central_laboratory_ids!= "{NULL}")\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .first()
                if others_certifications:
                    complete_details ['others_certifications'] = others_certifications.input
            return complete_details
        finally:
            db.close()           
    def get_sites_rec_hospital_infra_services(self,site_id,category_id):
        db = next(get_db())
        try:
            services = db.query(Site_Services.service_id, Site_Services.site_id, Site_Services.service_category,Site_Services.services,SiteServices.service_category_description)\
                .join(SiteServices,SiteServices.site_ser_id == Site_Services.services)\
                .filter(Site_Services.service_category == category_id)\
                .filter(Site_Services.site_id == site_id)\
                .all()
            return {"services" :services}
        finally:
            db.close()             
    def update_sites_rec_hospital_infra(self, site_id, update_hospital_infra):
        db = next(get_db())
        try:
            if update_hospital_infra.questionary:
                for questionary in update_hospital_infra.questionary:
                        question_id = db.query(Questionnaire).filter(Questionnaire.question == questionary.question).first()
                        existing_question_id = db.query(SiteRecHospitalInfra).filter(SiteRecHospitalInfra.site_id == site_id, SiteRecHospitalInfra.question == question_id.questionnaire_id).first()
                        if questionary.answer :
                            miscellaneous_val = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == questionary.answer.lower()).first()
                        if question_id:
                            if existing_question_id:
                                if question_id.type == "number" :
                                    existing_question_id.question = question_id.questionnaire_id,
                                    existing_question_id.input = questionary.inputvalue,
                                    existing_question_id.updated_by_id = update_hospital_infra.updated_by_id
                                    db.commit()                    
                                else:
                                    existing_question_id.question = question_id.questionnaire_id,
                                    existing_question_id.answer = miscellaneous_val.miscellaneous_id,
                                    existing_question_id.updated_by_id = update_hospital_infra.updated_by_id
                                    db.commit()
                            else:
                                if question_id.type == "number" :
                                    new_hosp_infra = SiteRecHospitalInfra(
                                            site_id = site_id,
                                            question = question_id.questionnaire_id,
                                            input = questionary.inputvalue,
                                            created_by_id = update_hospital_infra.updated_by_id
                                    )
                                    db.add(new_hosp_infra)
                                    db.commit()
                                else :
                                    new_hospital_infra = SiteRecHospitalInfra(
                                        site_id = site_id,
                                        question = question_id.questionnaire_id,
                                        answer = miscellaneous_val.miscellaneous_id,
                                        created_by_id = update_hospital_infra.updated_by_id
                                    )
                                    db.add(new_hospital_infra)
                                    db.commit()
            if update_hospital_infra.service:
                for checked in update_hospital_infra.service:
                    servics = db.query(SiteRecHospitalInfra)\
                        .filter(SiteRecHospitalInfra.services != {})\
                        .filter(SiteRecHospitalInfra.site_id == site_id)\
                        .first()
                    if servics:
                        servics.service_category_id = checked.service_category
                        servics.services = checked.services
                        servics.updated_by_id = update_hospital_infra.updated_by_id 
                        db.commit()
                    else :
                        new_diagnostic = SiteRecHospitalInfra(
                            site_id = site_id,
                            service_category_id = checked.service_category,
                            services = checked.services,
                            created_by_id = update_hospital_infra.updated_by_id
                        )
                        db.add(new_diagnostic)
                        db.commit()
            if update_hospital_infra.certifications:
                certificates = db.query(SiteRecHospitalInfra)\
                .filter(SiteRecHospitalInfra.certification_of_central_laboratory_ids != {})\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .first()
                if certificates :
                    certificates.certification_of_central_laboratory_ids = update_hospital_infra.certifications
                    certificates.updated_by_id = update_hospital_infra.updated_by_id
                    db.commit()
                else:
                    new_certifications = SiteRecHospitalInfra(
                        site_id = site_id,
                        certification_of_central_laboratory_ids = update_hospital_infra.certifications,
                        # input = update_hospital_infra.others_certifications,
                        created_by_id = update_hospital_infra.updated_by_id
                    )
                    db.add(new_certifications)
                    db.commit()
            if update_hospital_infra.equipment:
                equipments = db.query(SiteRecHospitalInfra)\
                .filter(SiteRecHospitalInfra.equipment_available_ids != {})\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .first()
                if equipments :
                    if update_hospital_infra.equipment:
                        equipments.equipment_available_ids = update_hospital_infra.equipment
                        equipments.updated_by_id = update_hospital_infra.updated_by_id
                        db.commit()
                else:
                    new_equipment = SiteRecHospitalInfra(
                        site_id = site_id,
                        equipment_available_ids = update_hospital_infra.equipment,
                        created_by_id = update_hospital_infra.updated_by_id
                    )
                    db.add(new_equipment)
                    db.commit() 
            if  update_hospital_infra.others_certifications is not None:
                input_data = db.query(SiteRecHospitalInfra)\
                .filter(SiteRecHospitalInfra.certification_of_central_laboratory_ids != {})\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .first()
                if input_data:
                    input_data.input = update_hospital_infra.others_certifications
                    input_data.updated_by_id = update_hospital_infra.updated_by_id
                    db.commit()
            return {"success" : "Hospital infra updated Successfully"}       
        finally:
            db.close()