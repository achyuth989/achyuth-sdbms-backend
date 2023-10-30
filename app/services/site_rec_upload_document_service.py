from app.model.site_rec_hospital_infra import SiteRecHospitalInfra
from app.model.site_certifications import Site_Certifications
from app.model.miscellaneous import Miscellaneous
from app.model.questionnaire import Questionnaire
from app.model.service_category import Service_Category
from app.model.services import Site_Services
from app.model.site_services import SiteServices
from app.model.md_equipments_site import Md_Equipments_Site
from app.model.cr_infra_site_rec import Cr_infra
from app.model.site_rec_hr import Siterec_hr
from app.model.cr import Cr
from app.model.it import It
from app.model.study_phases import StudyPhases
from app.model.research_product import Research_Product
from app.model.regulatory_info_site_rec import RegulatoryInfo
from app.model.document_category import DocumentCategory
from app.model.document_status import Document_Status
from app.model.upload_documents import Upload_Documents
from app.model.rec_population_grp import Rec_Population_grp
from app.model.population_group import Population_Group
from app.model.site import Site
from app.db.database import get_db
from sqlalchemy import and_ , func, or_ , desc
import re

class Site_Rec_Upload_documents:
    def get_sites_rec_deatils(self,site_id):
        db = next(get_db())
        miscellaneous_checked = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "answer", Miscellaneous.value == "yes")).first()
        miscellaneous_document_source = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "document source", Miscellaneous.value == "Electronic")).first()
        miscellaneous_document_source1 = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "document source", Miscellaneous.value == "Paper")).first()
        miscellaneous_health_record= db.query(Miscellaneous).filter(and_(Miscellaneous.type == "health record", Miscellaneous.value == "Developed by site")).first()
        miscellaneous_other = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "answer", Miscellaneous.value == "other")).first()
        site_rec_details = {}
        try:
            # population_served = db.query(Rec_Population_grp.pop_service_on_site_id).filter(Rec_Population_grp.site_id == site_id).filter(Rec_Population_grp.pop_service_on_site_id != {}).first()
            # population_list = []
            # if  population_served :  
            #     population_served_id = population_served[0]
            #     for num in population_served_id:
            #         population_served_details = db.query(Population_Group).filter(Population_Group.population_group_served_id == int(num)).first()
            #         population_list.append(population_served_details)
            #     if population_list :
            #         site_rec_details["Population_Served_on_Site"] = population_list

            cost_list = db.query(Questionnaire).filter(Questionnaire.question == "Cost List Available").first()

            # questions = db.query(SiteRecHospitalInfra.site_rec_hospital_infra_id,SiteRecHospitalInfra.site_id,SiteRecHospitalInfra.question,SiteRecHospitalInfra.answer,Questionnaire.questionnaire_id, Questionnaire.question)\
            #     .join(Questionnaire, SiteRecHospitalInfra.question == Questionnaire.questionnaire_id)\
            #     .filter(SiteRecHospitalInfra.answer == miscellaneous_checked.miscellaneous_id)\
            #     .filter(SiteRecHospitalInfra.question != cost_list.questionnaire_id)\
            #     .filter(SiteRecHospitalInfra.site_id == site_id)\
            #     .all()
            # if questions:
            #     site_rec_details["Hospital_Infra_Services"] = questions

            certificates = db.query(SiteRecHospitalInfra.certification_of_central_laboratory_ids)\
                .filter(SiteRecHospitalInfra.certification_of_central_laboratory_ids != "{NULL}")\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .first()
            certificate_list = []
            if certificates:
                certification_list = list(map(int, certificates[0]))
                # certificate_type_id = certificates[0][0]
                # for num in certificate_type_id.split(","):
                #     certificate_details = db.query(Site_Certifications).filter(Site_Certifications.site_certification_id == int(num)).first()
                #     certificate_list.append(certificate_details)
                for num in certification_list:
                    certificate_details = db.query(Site_Certifications).filter(Site_Certifications.site_certification_id == int(num)).first()
                    certificate_list.append(certificate_details)
                if certificate_list :
                    site_rec_details["Certifications_of_the_Sites_Central_Laboratory"] = certificate_list

            # servics = db.query(SiteRecHospitalInfra.service_category_id, SiteRecHospitalInfra.services)\
            #         .filter(SiteRecHospitalInfra.services != "{NULL}")\
            #         .filter(SiteRecHospitalInfra.site_id == site_id)\
            #         .all()
            # if servics:
            #     services_all_list = []
            #     for recservics in servics:
            #         category_id = recservics.service_category_id
            #         categorys = db.query(Service_Category)\
            #         .filter(Service_Category.service_category_id == category_id)\
            #         .first()
            #         service_type_id = recservics.services
            #         service_type_ids = ','.join(str(num) for num in service_type_id)
            #         services_list = []
            #         for num in service_type_ids.split(",") :
            #             services_details = db.query(Site_Services.service_id,SiteServices.service_category_description)\
            #             .join(SiteServices, SiteServices.site_ser_id == Site_Services.services)\
            #             .filter(Site_Services.service_id == int(num)).first()
            #             services_list.append(services_details)
            #         obj = {
            #             "service_category_id" : categorys.service_category_id,
            #             "service_category": categorys.service_category,
            #             "category_description" : categorys.description,
            #             "services_list" : services_list
            #         }
            #         services_all_list.append(obj)
            #         if services_all_list:
            #             site_rec_details['Diagnostic_and_imaging_services_performed_on_the_Site'] = services_all_list

            # equipment = db.query(SiteRecHospitalInfra.equipment_available_ids)\
            #     .filter(SiteRecHospitalInfra.equipment_available_ids != "{NULL}")\
            #     .filter(SiteRecHospitalInfra.site_id == site_id)\
            #     .first()
            # if equipment:
            #     equipment_list = []
            #     # equipment_type_id = equipment[0][0]
            #     # for num in equipment_type_id.split(","):
            #     equipment_type_id = list(map(int, equipment[0]))
            #     for num in equipment_type_id:
            #         equipment_details = db.query(Md_Equipments_Site).filter(Md_Equipments_Site.md_equipment_site_id == int(num)).first()
            #         equipment_list.append(equipment_details)
            #     if equipment_list :
            #         site_rec_details['Equipment_available_at_the_clinical_research_support_site'] = equipment_list

            cost_list_que = db.query(SiteRecHospitalInfra.site_rec_hospital_infra_id,SiteRecHospitalInfra.site_id,SiteRecHospitalInfra.question,SiteRecHospitalInfra.answer, Questionnaire.questionnaire_id, Questionnaire.question)\
                .join(Questionnaire, SiteRecHospitalInfra.question == Questionnaire.questionnaire_id)\
                .filter(SiteRecHospitalInfra.question == cost_list.questionnaire_id)\
                .filter(SiteRecHospitalInfra.answer == miscellaneous_checked.miscellaneous_id)\
                .filter(SiteRecHospitalInfra.site_id == site_id)\
                .first()
            if cost_list_que:
                site_rec_details["Cost_List_for_Services"] = cost_list_que
            
            # cr_infra_questions = db.query(Cr_infra.site_rec_cr_infra_id,Cr_infra.site_id,Cr_infra.question,Cr_infra.answer,Questionnaire.questionnaire_id, Questionnaire.question)\
            #     .join(Questionnaire, Cr_infra.question == Questionnaire.questionnaire_id)\
            #     .filter(Cr_infra.answer == miscellaneous_checked.miscellaneous_id)\
            #     .filter(Cr_infra.site_id == site_id)\
            #     .all()
            # if cr_infra_questions:
            #     site_rec_details["Clinical_Research_Infra_Capabilities"] = cr_infra_questions

            # cr_phases = db.query(Cr_infra.phase_study_ids).filter(Cr_infra.phase_study_ids != " ")\
            # .filter(Cr_infra.site_id == site_id).first()
            # if cr_phases :
            #     list_exp = cr_phases[0].split(',')
            #     ids = [eval(i) for i in list_exp]
            #     phase_list=[]
            #     for phase_id in ids:
            #         study_phases = db.query(StudyPhases.phases_type,StudyPhases.study_phase_id).filter(StudyPhases.study_phase_id == phase_id).first()
            #         phase_list.append(study_phases)
            #     if phase_list:
            #         site_rec_details["Capacity_to_participate_in_phase_clinical_studies"] = phase_list

            # cr_research_products = db.query(Cr_infra.research_product_ids).filter(Cr_infra.research_product_ids != " ").filter(Cr_infra.site_id == site_id).first()
            # if cr_research_products :
            #     list_pro = cr_research_products[0].split(',')
            #     ids = [eval(i) for i in list_pro]
            #     cr_products=[]
            #     if cr_research_products:
            #         for product_id in ids:
            #             research_products = db.query(Research_Product.research_product_id,Research_Product.research_product_type).filter(Research_Product.research_product_id == product_id).first()
            #             cr_products.append(research_products)
            #         if cr_products:
            #             site_rec_details["Capacity_for_preparation_and_administration_of_research_products"] = cr_products

            # it_infra_questions = db.query(It.site_rec_it_systems_infra_id,It.site_id,It.question,It.answer,Questionnaire.questionnaire_id, Questionnaire.question)\
            #     .join(Questionnaire, It.question == Questionnaire.questionnaire_id)\
            #     .filter(or_(It.answer == miscellaneous_checked.miscellaneous_id,
            #                 It.answer == miscellaneous_document_source.miscellaneous_id,
            #                 It.answer == miscellaneous_document_source1.miscellaneous_id,
            #                 It.answer == miscellaneous_health_record.miscellaneous_id,
            #                 It.answer == miscellaneous_other.miscellaneous_id ))\
            #     .filter(It.site_id == site_id)\
            #     .all()
            # if it_infra_questions:
            #     site_rec_details["IT_Systems_Infra"] = it_infra_questions
            
            hr_questions = db.query(Siterec_hr.site_rec_hr_id,Siterec_hr.site_id,Siterec_hr.question,Siterec_hr.answer,Questionnaire.questionnaire_id, Questionnaire.question)\
                .join(Questionnaire, Siterec_hr.question == Questionnaire.questionnaire_id)\
                .filter(Siterec_hr.answer == miscellaneous_checked.miscellaneous_id)\
                .filter(Siterec_hr.site_id == site_id)\
                .all()
            if hr_questions:
                site_rec_details["Human_Resources"] = hr_questions

            miscellaneous_availability = db.query(Miscellaneous)\
            .filter(and_(Miscellaneous.type == "doc_status" , Miscellaneous.value == "available" ))\
            .first()
            # regulatory_info_details = db.query(RegulatoryInfo)\
            # .filter(RegulatoryInfo.availability == miscellaneous_availability.miscellaneous_id)\
            # .filter(RegulatoryInfo.site_id == site_id).all()
            regulatory_info_details = db.query(DocumentCategory.description,RegulatoryInfo.document)\
            .join(DocumentCategory, DocumentCategory.document_category_id == RegulatoryInfo.document_category_id)\
            .filter(RegulatoryInfo.availability == miscellaneous_availability.miscellaneous_id)\
            .filter(RegulatoryInfo.site_id == site_id).all()
            if regulatory_info_details:
                all_records = {}
                for details in regulatory_info_details:
                    # if details.description not in all_records:
                    #     all_records[details.description] = []
                    # all_records[details.description].append(details)
                    description = details.description
                    description = re.sub(r'\W+', '_', description).strip('_')
                    if description not in all_records:
                        all_records[description] = []
                    all_records[description].append(details)
                if all_records:
                    site_rec_details["Regulatory_Information"] = all_records
                # all_records = []
                # for details in regulatory_info_details:
                #     document_category_record = db.query(DocumentCategory).filter(DocumentCategory.document_category_id== details.document_category_id).first()
                #     status_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id== details.availability).first()
                    
                #     details.document_category_description = document_category_record.description
                #     details.document_status = status_record.value
                   
                #     all_records.append(details)
                # if all_records:
                #     site_rec_details["Regulatory_Information"] = all_records
            return site_rec_details
        finally:
            db.close()
    def add_sites_rec_upload_documents(self,data):
        db = next(get_db())
        try:  
            # if data.Site_Population :
            #     populationdetails = []
            #     for population in data.Site_Population : 
            #         attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == population.document_attached).first() 
            #         # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == population.document_name, Upload_Documents.screen_label_name == "Population Served on Site").filter(Upload_Documents.site_id == data.site_id).first()
            #         existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == population.docid).first()
            #         if existed_id:
            #             existed_id.document_attached = attached_id.miscellaneous_id,
            #             existed_id.version = population.version,
            #             existed_id.status = population.status,
            #             existed_id.remarks = population.remarks,
            #             existed_id.attachment = population.attachment,
            #             existed_id.updated_by_id = data.created_by_id
            #             db.commit()
            #         else:    
            #             population_upload_doc = Upload_Documents(
            #                 site_id = data.site_id,
            #                 screen_type_name = "Site Recognition",
            #                 screen_label_name = "Population Served on Site",
            #                 document_name = population.document_name,
            #                 document_attached = attached_id.miscellaneous_id,
            #                 version = population.version,
            #                 status = population.status,
            #                 remarks = population.remarks,
            #                 attachment = population.attachment,
            #                 created_by_id = data.created_by_id
            #             )
            #             populationdetails.append(population_upload_doc)
            #     db.add_all(populationdetails)
            #     db.commit()

            # if data.Hospital_Infra :
            #     hospitalinfradetails = []
            #     for hospitalinfra in data.Hospital_Infra : 
            #         attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == hospitalinfra.document_attached).first() 
            #         # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == hospitalinfra.document_name, Upload_Documents.screen_label_name == "Hospital Infra & Services").filter(Upload_Documents.site_id == data.site_id).first()
            #         existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == hospitalinfra.docid).first()
            #         if existed_id:
            #             existed_id.document_attached = attached_id.miscellaneous_id,
            #             existed_id.version = hospitalinfra.version,
            #             existed_id.status = hospitalinfra.status,
            #             existed_id.remarks = hospitalinfra.remarks,
            #             existed_id.attachment = hospitalinfra.attachment,
            #             existed_id.updated_by_id = data.created_by_id
            #             db.commit()
            #         else:
            #             hospital_upload_doc = Upload_Documents(
            #                 site_id = data.site_id,
            #                 screen_type_name = "Site Recognition",
            #                 screen_label_name = "Hospital Infra & Services",
            #                 document_name = hospitalinfra.document_name,
            #                 document_attached = attached_id.miscellaneous_id,
            #                 version = hospitalinfra.version,
            #                 status = hospitalinfra.status,
            #                 remarks = hospitalinfra.remarks,
            #                 attachment = hospitalinfra.attachment,
            #                 created_by_id = data.created_by_id
            #             )
            #             hospitalinfradetails.append(hospital_upload_doc)
            #     db.add_all(hospitalinfradetails)
            #     db.commit()

            # if data.services :
            #     services = []
            #     for hospitalinfraservices in data.services : 
            #         attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == hospitalinfraservices.document_attached).first()  
            #         # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == hospitalinfraservices.document_name, Upload_Documents.screen_label_name == "Diagnostic and imaging services performed on the Site").filter(Upload_Documents.site_id == data.site_id).first()
            #         existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == hospitalinfraservices.docid).first()
            #         if existed_id:
            #             existed_id.document_attached = attached_id.miscellaneous_id,
            #             existed_id.version = hospitalinfraservices.version,
            #             existed_id.status = hospitalinfraservices.status,
            #             existed_id.remarks = hospitalinfraservices.remarks,
            #             existed_id.attachment = hospitalinfraservices.attachment,
            #             existed_id.updated_by_id = data.created_by_id
            #             db.commit()
            #         else:
            #             hospital_services_doc = Upload_Documents(
            #                 site_id = data.site_id,
            #                 screen_type_name = "Site Recognition",
            #                 screen_label_name = "Diagnostic and imaging services performed on the Site",
            #                 document_name = hospitalinfraservices.document_name,
            #                 document_attached = attached_id.miscellaneous_id,
            #                 version = hospitalinfraservices.version,
            #                 status = hospitalinfraservices.status,
            #                 remarks = hospitalinfraservices.remarks,
            #                 attachment = hospitalinfraservices.attachment,
            #                 created_by_id = data.created_by_id
            #             )
            #             services.append(hospital_services_doc)
            #     db.add_all(services)
            #     db.commit()
            site_id = data.site_id
            created_by_id = data.created_by_id

            

            if data.Certifications : 
                certifications = []
                for doc in data.Certifications : 
                    
                    attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == doc.document_attached).first()      
                    for version in doc.versions:
                        
                            # attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == doc.document_attached).first()      
                            # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == hospitalinfracertifications.document_name, Upload_Documents.screen_label_name == "Certifications of the Site'S Central Laboratory").filter(Upload_Documents.site_id == data.site_id).first()
                        existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == version.upload_document_id).first()
                        if existed_id:
                            
                            existed_id.document_attached = attached_id.miscellaneous_id,
                            existed_id.version = version.version,
                            existed_id.status = version.status,
                            existed_id.remarks = doc.remarks,
                            existed_id.attachment = version.attachment,
                            existed_id.updated_by_id = created_by_id
                            db.commit()
                        else:
                            
                            hospital_certifications_doc = Upload_Documents(
                                    site_id = site_id,
                                    screen_type_name = "Site Recognition",
                                    screen_label_name = "Certifications of the Site'S Central Laboratory",
                                    document_name = doc.document_name,
                                    document_attached = attached_id.miscellaneous_id,
                                    version = version.version,
                                    status = version.status,
                                    remarks = doc.remarks,
                                    attachment = version.attachment,
                                    created_by_id = created_by_id
                                )
                            certifications.append(hospital_certifications_doc)                       
                
                    db.add_all(certifications)
                    db.commit()

            # if data.Equipment :  
            #     equipment = []
            #     for hospitalinfraequipment in data.Equipment : 
            #         attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == hospitalinfraequipment.document_attached).first()  
            #         # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == hospitalinfraequipment.document_name, Upload_Documents.screen_label_name == "Equipment available at the clinical research support site").filter(Upload_Documents.site_id == data.site_id).first()
            #         existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == hospitalinfraequipment.docid).first()
            #         if existed_id:
            #             existed_id.document_attached = attached_id.miscellaneous_id,
            #             existed_id.version = hospitalinfraequipment.version,
            #             existed_id.status = hospitalinfraequipment.status,
            #             existed_id.remarks = hospitalinfraequipment.remarks,
            #             existed_id.attachment = hospitalinfraequipment.attachment,
            #             existed_id.updated_by_id = data.created_by_id
            #             db.commit()
            #         else:
            #             hospital_equipment_doc = Upload_Documents(
            #                 site_id = data.site_id,
            #                 screen_type_name = "Site Recognition",
            #                 screen_label_name = "Equipment available at the clinical research support site",
            #                 document_name = hospitalinfraequipment.document_name,
            #                 document_attached = attached_id.miscellaneous_id,
            #                 version = hospitalinfraequipment.version,
            #                 status = hospitalinfraequipment.status,
            #                 remarks = hospitalinfraequipment.remarks,
            #                 attachment = hospitalinfraequipment.attachment,
            #                 created_by_id = data.created_by_id
            #             )
            #             equipment.append(hospital_equipment_doc)
            #     db.add_all(equipment)
            #     db.commit()

            if data.Cost_List :  
                Costlist = []
                for costlist in data.Cost_List :
                    attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == costlist.document_attached).first()  
                    for version in costlist.versions:
                    
                    # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == costlist.document_name, Upload_Documents.screen_label_name == "Cost List for Services").filter(Upload_Documents.site_id == data.site_id).first()
                        existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == version.upload_document_id).first()
                        if existed_id:
                            existed_id.document_attached = attached_id.miscellaneous_id,
                            existed_id.version = version.version,
                            existed_id.status = version.status,
                            existed_id.remarks = costlist.remarks,
                            existed_id.attachment = version.attachment,
                            existed_id.updated_by_id = created_by_id
                            db.commit()
                        else:
                            costlist_doc = Upload_Documents(
                                site_id = site_id,
                                screen_type_name = "Site Recognition",
                                screen_label_name = "Cost List for Services",
                                document_name = costlist.document_name,
                                document_attached = attached_id.miscellaneous_id,
                                version = version.version,
                                status = version.status,
                                remarks = costlist.remarks,
                                attachment = version.attachment,
                                created_by_id = created_by_id
                            )
                            Costlist.append(costlist_doc)
                db.add_all(Costlist)
                db.commit()

            # if data.Cr_Infra :
            #     cr_infra = []
            #     for crinfra in data.Cr_Infra :  
            #         attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == crinfra.document_attached).first() 
            #         # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == crinfra.document_name, Upload_Documents.screen_label_name == "Clinical Research Infra & Capabilities").filter(Upload_Documents.site_id == data.site_id).first()
            #         existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == crinfra.docid).first()
            #         if existed_id:
            #             existed_id.document_attached = attached_id.miscellaneous_id,
            #             existed_id.version = crinfra.version,
            #             existed_id.status = crinfra.status,
            #             existed_id.remarks = crinfra.remarks,
            #             existed_id.attachment = crinfra.attachment,
            #             existed_id.updated_by_id = data.created_by_id
            #             db.commit()
            #         else:
            #             hospital_cr_infra_doc = Upload_Documents(
            #                 site_id = data.site_id,
            #                 screen_type_name = "Site Recognition",
            #                 screen_label_name = "Clinical Research Infra & Capabilities",
            #                 document_name = crinfra.document_name,
            #                 document_attached = attached_id.miscellaneous_id,
            #                 version = crinfra.version,
            #                 status = crinfra.status,
            #                 remarks = crinfra.remarks,
            #                 attachment = crinfra.attachment,
            #                 created_by_id = data.created_by_id
            #             )
            #             cr_infra.append(hospital_cr_infra_doc)
            #     db.add_all(cr_infra)
            #     db.commit()

            # if data.Cr_Infra_Phases :  
            #     cr_infra_phases = []
            #     for phases in data.Cr_Infra_Phases :  
            #         attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == phases.document_attached).first() 
            #         # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == phases.document_name, Upload_Documents.screen_label_name == "Capacity to participate in phase clinical studies").filter(Upload_Documents.site_id == data.site_id).first()
            #         existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == phases.docid).first()
            #         if existed_id:
            #             existed_id.document_attached = attached_id.miscellaneous_id,
            #             existed_id.version = phases.version,
            #             existed_id.status = phases.status,
            #             existed_id.remarks = phases.remarks,
            #             existed_id.attachment = phases.attachment,
            #             existed_id.updated_by_id = data.created_by_id
            #             db.commit()
            #         else:
            #             phases_doc = Upload_Documents(
            #                 site_id = data.site_id,
            #                 screen_type_name = "Site Recognition",
            #                 screen_label_name = "Capacity to participate in phase clinical studies",
            #                 document_name = phases.document_name,
            #                 document_attached = attached_id.miscellaneous_id,
            #                 version = phases.version,
            #                 status = phases.status,
            #                 remarks = phases.remarks,
            #                 attachment = phases.attachment,
            #                 created_by_id = data.created_by_id
            #             )
            #             cr_infra_phases.append(phases_doc)
            #     db.add_all(cr_infra_phases)
            #     db.commit()

            # if data.Cr_Infra_Research_Products : 
            #     research_products = []
            #     for researchproducts in data.Cr_Infra_Research_Products : 
            #         attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == researchproducts.document_attached).first()  
            #         # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == researchproducts.document_name, Upload_Documents.screen_label_name == "Capacity for preparation and administration of research products").filter(Upload_Documents.site_id == data.site_id).first()
            #         existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == researchproducts.docid).first()
            #         if existed_id:
            #             existed_id.document_attached = attached_id.miscellaneous_id,
            #             existed_id.version = researchproducts.version,
            #             existed_id.status = researchproducts.status,
            #             existed_id.remarks = researchproducts.remarks,
            #             existed_id.attachment = researchproducts.attachment,
            #             existed_id.updated_by_id = data.created_by_id
            #             db.commit()
            #         else:
            #             hospital_products_doc = Upload_Documents(
            #                 site_id = data.site_id,
            #                 screen_type_name = "Site Recognition",
            #                 screen_label_name = "Capacity for preparation and administration of research products",
            #                 document_name = researchproducts.document_name,
            #                 document_attached = attached_id.miscellaneous_id,
            #                 version = researchproducts.version,
            #                 status = researchproducts.status,
            #                 remarks = researchproducts.remarks,
            #                 attachment = researchproducts.attachment,
            #                 created_by_id = data.created_by_id
            #             )
            #             research_products.append(hospital_products_doc)
            #     db.add_all(research_products)
            #     db.commit()

            # if data.IT_Systems_Infra :
            #     it_infra = []
            #     for itinfra in data.IT_Systems_Infra :  
            #         attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == itinfra.document_attached).first() 
            #         # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == itinfra.document_name, Upload_Documents.screen_label_name == "IT & Systems Infra").filter(Upload_Documents.site_id == data.site_id).first()
            #         existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == itinfra.docid).first()
            #         if existed_id:
            #             existed_id.document_attached = attached_id.miscellaneous_id,
            #             existed_id.version = itinfra.version,
            #             existed_id.status = itinfra.status,
            #             existed_id.remarks = itinfra.remarks,
            #             existed_id.attachment = itinfra.attachment,
            #             existed_id.updated_by_id = data.created_by_id
            #             db.commit()
            #         else:
            #             hospital_itinfra_doc = Upload_Documents(
            #                 site_id = data.site_id,
            #                 screen_type_name = "Site Recognition",
            #                 screen_label_name = "IT & Systems Infra",
            #                 document_name = itinfra.document_name,
            #                 document_attached = attached_id.miscellaneous_id,
            #                 version = itinfra.version,
            #                 status = itinfra.status,
            #                 remarks = itinfra.remarks,
            #                 attachment = itinfra.attachment,
            #                 created_by_id = data.created_by_id
            #             )
            #             it_infra.append(hospital_itinfra_doc)
            #     db.add_all(it_infra)
            #     db.commit()

            if data.Human_Resources :
                hr_list = []
                for hrdetails in data.Human_Resources : 
                    attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == hrdetails.document_attached).first() 
                    for version in  hrdetails.versions:
                    
                    # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == hrdetails.document_name, Upload_Documents.screen_label_name == "Human Resources").filter(Upload_Documents.site_id == data.site_id).first()
                        existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == version.upload_document_id).first()
                        if existed_id:
                            existed_id.document_attached = attached_id.miscellaneous_id,
                            existed_id.version = version.version,
                            existed_id.status = version.status,
                            existed_id.remarks = hrdetails.remarks,
                            existed_id.attachment = version.attachment,
                            existed_id.updated_by_id = created_by_id
                            db.commit()
                        else:
                            hr_doc = Upload_Documents(
                                site_id = site_id,
                                screen_type_name = "Site Recognition",
                                screen_label_name = "Human Resources",
                                document_name = hrdetails.document_name,
                                document_attached = attached_id.miscellaneous_id,
                                version = version.version,
                                status = version.status,
                                remarks = hrdetails.remarks,
                                attachment = version.attachment,
                                created_by_id = created_by_id
                            )
                            hr_list.append(hr_doc)
                db.add_all(hr_list)
                db.commit()

            if data.Regulatory_Information :
                regulatory_information = []
                for reginfo in data.Regulatory_Information : 
                    attached_id = db.query(Miscellaneous).filter(Miscellaneous.value == reginfo.document_attached).first() 
                    for version in reginfo.versions:
                    
                    # existed_id = db.query(Upload_Documents).filter(Upload_Documents.document_name == reginfo.document_name, Upload_Documents.screen_label_name == reginfo.category).filter(Upload_Documents.site_id == data.site_id).first()
                        existed_id = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == version.upload_document_id).first()
                        if existed_id:
                            existed_id.document_attached = attached_id.miscellaneous_id,
                            existed_id.version = version.version,
                            existed_id.status = version.status,
                            existed_id.remarks = reginfo.remarks,
                            existed_id.attachment = version.attachment,
                            existed_id.updated_by_id = created_by_id
                            db.commit()
                        else:
                            reginfo_doc = Upload_Documents(
                                site_id = site_id,
                                screen_type_name = "Site Recognition",
                                screen_label_name = reginfo.category,
                                document_name = reginfo.document_name,
                                document_attached = attached_id.miscellaneous_id,
                                version = version.version,
                                status = version.status,
                                remarks = reginfo.remarks,
                                attachment = version.attachment,
                                created_by_id = created_by_id
                            )
                            regulatory_information.append(reginfo_doc)
                db.add_all(regulatory_information)
                db.commit()
            return "details added"
        finally:
            db.close()   
    def get_sites_rec_upload_documents(self,site_id):
        db = next(get_db())
        try:
            details = {}
            # population = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == site_id)\
            # .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            # .filter(Upload_Documents.screen_label_name == "Population Served on Site").all()
            # if population:
            #     details["Population_Served_on_Site"] = population

            # hospitalinfra = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == site_id)\
            # .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            # .filter(Upload_Documents.screen_label_name == "Hospital Infra & Services").all()
            # if hospitalinfra:
            #     details["Hospital_Infra_Services"] = hospitalinfra
            
            # services = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == site_id)\
            # .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            # .filter(Upload_Documents.screen_label_name == "Diagnostic and imaging services performed on the Site").all()
            # if services:
            #     details["Diagnostic_and_imaging_services"] = services
            
            certifications = db.query(Upload_Documents.site_id,Upload_Documents.screen_label_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Upload_Documents.document_attached,Miscellaneous.value,Document_Status.document_status_description)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            .filter(Upload_Documents.site_id == site_id)\
            .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            .filter(Upload_Documents.screen_label_name == "Certifications of the Site'S Central Laboratory").order_by(desc(Upload_Documents.created)).all()
            # if certifications:
            #     details["Certifications_of_the_site_central_laboratory"] = certifications

            certification_document_dict = {}
            for result in certifications:
                document_name = result.document_name
                if document_name not in certification_document_dict:
                    certification_document_dict[document_name] = {
                        "site_id": result.site_id,
                        # "cr_id": result.cr_code,
                        "screen_label_name": result.screen_label_name,
                        "document_name": document_name,
                        "value": result.value,
                        # "status": result.status,
                        "remarks": result.remarks,
                        "versions": []
                    }
                certification_document_dict[document_name]["versions"].append({
                    "upload_document_id": result.upload_document_id,
                    "version": result.version,
                    "attachment": result.attachment,
                    "status": result.status,
                })

            # Convert the dictionary values to a list
            grouped_results = list(certification_document_dict.values())

            if grouped_results:
                details["Certifications_of_the_site_central_laboratory"] = grouped_results   
            
            # equipment = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == site_id)\
            # .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            # .filter(Upload_Documents.screen_label_name == "Equipment available at the clinical research support site").all()
            # if equipment:
            #     details["Equipment_available_at_the_clinical_research_support_site"] = equipment

            costlist = db.query(Upload_Documents.site_id,Upload_Documents.screen_label_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Upload_Documents.document_attached,Miscellaneous.value,Document_Status.document_status_description)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            .filter(Upload_Documents.site_id == site_id)\
            .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            .filter(Upload_Documents.screen_label_name == "Cost List for Services").order_by(desc(Upload_Documents.created)).all()
            # if costlist:
            #     details["Cost_List_for_Services"] = costlist

            costlist_document_dict = {}
            for result in costlist:
                document_name = result.document_name
                if document_name not in costlist_document_dict:
                    costlist_document_dict[document_name] = {
                        "site_id": result.site_id,
                        # "cr_id": result.cr_code,
                        "screen_label_name": result.screen_label_name,
                        "document_name": document_name,
                        "value": result.value,
                        # "status": result.status,
                        "remarks": result.remarks,
                        "versions": []
                    }
                costlist_document_dict[document_name]["versions"].append({
                    "upload_document_id": result.upload_document_id,
                    "version": result.version,
                    "attachment": result.attachment,
                    "status": result.status,
                })

            # Convert the dictionary values to a list
            costlist_results = list(costlist_document_dict.values())

            if costlist_results:
                details["Cost_List_for_Services"] = costlist_results
                    

            # cr = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == site_id)\
            # .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            # .filter(Upload_Documents.screen_label_name == "Clinical Research Infra & Capabilities").all()
            # if cr:
            #     details["Clinical_Research_Infra"] = cr

            # phases = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == site_id)\
            # .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            # .filter(Upload_Documents.screen_label_name == "Capacity to participate in phase clinical studies").all()
            # if phases:
            #     details["Clinical_Research_Infra_Phases"] = phases

            # products = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == site_id)\
            # .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            # .filter(Upload_Documents.screen_label_name == "Capacity for preparation and administration of research products").all()
            # if products:
            #     details["Cr_Infra_Research_Products"] = products

            # it_infra = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Miscellaneous.value,Document_Status.document_status_description)\
            # .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            # .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            # .filter(Upload_Documents.site_id == site_id)\
            # .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            # .filter(Upload_Documents.screen_label_name == "IT & Systems Infra").all()
            # if it_infra:
            #     details["IT_Systems_Infra"] = it_infra

            hr = db.query(Upload_Documents.site_id,Upload_Documents.screen_label_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Upload_Documents.document_attached,Miscellaneous.value,Document_Status.document_status_description)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            .filter(Upload_Documents.site_id == site_id)\
            .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            .filter(Upload_Documents.screen_label_name == "Human Resources").order_by(desc(Upload_Documents.created)).all()
            # if hr:
            #     details["Human_Resources"] = hr
            hr_document_dict = {}
            for result in hr:
                document_name = result.document_name
                if document_name not in hr_document_dict:
                    hr_document_dict[document_name] = {
                        "site_id": result.site_id,
                        # "cr_id": result.cr_code,
                        "screen_label_name": result.screen_label_name,
                        "document_name": document_name,
                        "value": result.value,
                        # "status": result.status,
                        "remarks": result.remarks,
                        "versions": []
                    }
                hr_document_dict[document_name]["versions"].append({
                    "upload_document_id": result.upload_document_id,
                    "version": result.version,
                    "attachment": result.attachment,
                    "status": result.status,
                })

            # Convert the dictionary values to a list
            hr_results = list(hr_document_dict.values())

            if hr_results:
                details["Human_Resources"] = hr_results

            
            regulatory = db.query(Upload_Documents.site_id,Upload_Documents.screen_type_name,Upload_Documents.screen_label_name,Upload_Documents.document_name,Upload_Documents.version,Upload_Documents.remarks,Upload_Documents.upload_document_id,Upload_Documents.status,Upload_Documents.attachment,Upload_Documents.document_attached,Miscellaneous.value,Document_Status.document_status_description)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Upload_Documents.document_attached)\
            .outerjoin(Document_Status, Document_Status.documentstatus_id == Upload_Documents.status)\
            .filter(Upload_Documents.site_id == site_id)\
            .filter(Upload_Documents.screen_type_name == "Site Recognition")\
            .filter(Upload_Documents.screen_label_name != "Population Served on Site")\
            .filter(Upload_Documents.screen_label_name != "Hospital Infra & Services")\
            .filter(Upload_Documents.screen_label_name != "Diagnostic and imaging services performed on the Site")\
            .filter(Upload_Documents.screen_label_name != "Certifications of the Site'S Central Laboratory")\
            .filter(Upload_Documents.screen_label_name != "Equipment available at the clinical research support site")\
            .filter(Upload_Documents.screen_label_name != "Cost List for Services")\
            .filter(Upload_Documents.screen_label_name != "Clinical Research Infra & Capabilities")\
            .filter(Upload_Documents.screen_label_name != "Capacity to participate in phase clinical studies")\
            .filter(Upload_Documents.screen_label_name != "Capacity for preparation and administration of research products")\
            .filter(Upload_Documents.screen_label_name != "IT & Systems Infra")\
            .filter(Upload_Documents.screen_label_name != "Human Resources").order_by(desc(Upload_Documents.created)).all()
            if regulatory:
                # details["Regulatory_Information"] = regulatory
                all_records_regulatory = {}
                # for record in regulatory:
                #     screen_label_name = record.screen_label_name
                #     screen_label_name = re.sub(r'\W+', '_', screen_label_name).strip('_')
                #     if screen_label_name not in all_records_regulatory:
                #         all_records_regulatory[screen_label_name] = []
                #     all_records_regulatory[screen_label_name].append(record)
                # if all_records_regulatory:
                #     # details.update(all_records_regulatory)
                #     details["Regulatory_Information"] = all_records_regulatory

                for result in regulatory:
                    document_name = result.document_name
                    if document_name not in all_records_regulatory:
                        all_records_regulatory[document_name] = {
                            "site_id": result.site_id,
                            # "cr_id": result.cr_code,
                            "screen_label_name": result.screen_label_name,
                            "document_name": document_name,
                            "value": result.value,
                            # "status": result.status,
                            "remarks": result.remarks,
                            "versions": []
                        }
                    all_records_regulatory[document_name]["versions"].append({
                        "upload_document_id": result.upload_document_id,
                        "version": result.version,
                        "attachment": result.attachment,
                        "status": result.status,
                    })

            # Convert the dictionary values to a list
                regulatory_results = list(all_records_regulatory.values())

                records_regulatory = {}
                for record in regulatory_results:
                    screen_label_name = record['screen_label_name']
                    screen_label_name = re.sub(r'\W+', '_', screen_label_name).strip('_')
                    if screen_label_name not in records_regulatory:
                        records_regulatory[screen_label_name] = []
                    records_regulatory[screen_label_name].append(record)
                if records_regulatory:
                    # details.update(records_regulatory)
                    details["Regulatory_Information"] = records_regulatory

                # if regulatory_results:
                #     details["Regulatory_Information"] = regulatory_results

            
            return {"details": details}
        finally:
            db.close()
    def get_sites_upload_status(self):
        db = next(get_db())
        active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
        sites_list = db.query(Site.site_id, Site.site_code, Site.site_name).filter(Site.status == active.miscellaneous_id).order_by(desc(Site.created)).all()
        try:
            if sites_list:
                sites  = []
                for sitestatus in sites_list:
                    status = ""
                    cr_list = db.query(Cr).filter(Cr.site_id == sitestatus.site_id).all()
                    site_rec = db.query(Upload_Documents).filter(Upload_Documents.site_id == sitestatus.site_id, Upload_Documents.screen_type_name == "Site Recognition").all()
                    site_assess = db.query(Upload_Documents).filter(Upload_Documents.site_id == sitestatus.site_id, Upload_Documents.screen_type_name == "Site Assessment").all()
                    cr_table = []
                    for cr_data in cr_list:
                        cr_codes = db.query(Upload_Documents).filter(Upload_Documents.site_id == sitestatus.site_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.cr_code == cr_data.site_rec_cr_id).all()
                        if cr_codes:
                            cr_table.append(cr_codes)
                    if site_rec and site_assess and len(cr_table) == len(cr_list):
                        status = "Completed"
                    elif site_rec or site_assess or cr_table:
                        status = "In Progress"
                    else :
                        status = "Not Started"
                    obj = {
                        "site_id" : sitestatus.site_id,
                        "site_code": sitestatus.site_code,
                        "site_name" : sitestatus.site_name,
                        "status" : status
                    }
                    sites.append(obj)
                return {"sites" : sites}
        finally:
            db.close()    