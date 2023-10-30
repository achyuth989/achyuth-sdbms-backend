from app.model.country_details import CountryDetails
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func, desc
from app.model.miscellaneous import Miscellaneous
from datetime import datetime
# from app.services.cr_professional_experience_service import Cr_Professional_Exp_Service
# from app.services.general_service import General_Service
from app.model.cr_gen_education import GeneralEducation
from app.model.cr_gen_facilities_affiliations import GeneralAffiliations
from app.model.general import General
from app.model.upload_documents import Upload_Documents
from app.model.cr_professional_experience import Cr_Research_Exp_Check_List, Cr_Professional_Experience,Cr_License_Ense, Cr_Gcp_Trai ,Cr_Specialities , Cr_Total_Clinical_Research_Exp
from app.model.specialities_subspecialities import SpecialitySubspeciality
from app.model.speciality import Speciality
from app.model.icd import Icd
from app.model.institution import Institution
from app.model.license_type import LicenseType
from app.model.study_phases import StudyPhases
from app.model.research_product import Research_Product
from app.model.study_type import Study_Type
from app.model.cr import Cr
from app.model.document_status import Document_Status
from app.model.cr_status import Cr_Status
from app.model.user import User


# cr_professional_exp_service = Cr_Professional_Exp_Service()
# general_service = General_Service()

class Upload_Doc_cr_Service:
    def get_cr_doc_details(self,cr_id):
        db = next(get_db())
        try:
            cr_docs = {}
            # education=db.query(GeneralEducation).join(General).filter(General.cr_code == cr_id)
            # education_details=education.all()
            # print(education_details)

            #for getting education docs
            query = f"SELECT edu.* \
            FROM cr_general gen \
            JOIN cr_gen_education edu ON gen.cr_general_id = edu.cr_general_id \
            WHERE gen.cr_general_id = {cr_id};"
            education = db.execute(query)
            education_details = education.fetchall()

            # affiliations=db.query(GeneralAffiliations).join(General).filter(General.cr_code == cr_id)
            # affiliations_details = affiliations.all()
            # print(affiliations_details)

            #for getting affiliations docs
            query1 = f"SELECT aff.* \
            FROM cr_general gen \
            JOIN cr_gen_facilities_affiliations aff ON gen.cr_general_id = aff.cr_general_id\
            WHERE gen.cr_general_id = {cr_id};"
            
            # for getting check list & research exp docs
            cr_checklist=db.query(Cr_Research_Exp_Check_List).filter(Cr_Research_Exp_Check_List.cr_general_id == cr_id).all()
            if cr_checklist:
                for data in cr_checklist:
                    # get clinical answer
                    if data.clinical_study_phases: 
                        phase_study_ids_list = data.clinical_study_phases.split(",")
                        phase_answer =[]
                        for ids in phase_study_ids_list: 
                            ids = int(ids)
                            phase_answer_record = db.query(StudyPhases).filter(StudyPhases.study_phase_id == ids).first()
                
                            answer = phase_answer_record.phases_type
                            phase_answer.append(answer)
                        data.clinical_study_phases_answer = phase_answer
                    else:
                        data.clinical_study_phases_answer = None
                           
                    # get study type answer  
                    if data.study_type:
                        study_type_ids_list = data.study_type.split(",")
                        study_type_answer =[]
                        for ids in study_type_ids_list:
                            ids = int(ids)
                            study_type_answer_record = db.query(Study_Type).filter(Study_Type.studytype_id == ids).first()
                            
                            answer = study_type_answer_record.study_type
                            study_type_answer.append(answer)
                        data.study_type_answer= study_type_answer
                    else:
                        data.study_type_answer= None
                            
                        
                    # get cv answer
                    if data.cv:
                        cv_answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==data.cv).first()
                        cv_answer = cv_answer_record.value
                        data.cv_answer= cv_answer 
                    else:
                        data.cv_answer= None
                        
                    # get scanned id answer
                    if data.scanned_id:      
                        scanned_id_answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==data.scanned_id).first()
                        scanned_id_answer = scanned_id_answer_record.value
                        data.scanned_id_answer= scanned_id_answer
                    else:
                        data.scanned_id_answer= None
                        
                    
                    # get scanned title answer
                    if data.scanned_title:
                        scanned_title_answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==data.scanned_title).first()
                        scanned_title_answer = scanned_title_answer_record.value
                        data.scanned_title_answer= scanned_title_answer
                    else:
                        data.scanned_title_answer= None
                    
                    
                    # get scanned_license answer
                    if data.scanned_license:
                        scanned_license_answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==data.scanned_license).first()
                        scanned_license_answer = scanned_license_answer_record.value
                        data.scanned_license_answer= scanned_license_answer
                    else:
                        data.scanned_license_answer= None
                        
                    # get IATA_training_answer
                    if data.IATA_training:
                        IATA_training_answer_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id==data.IATA_training).first()
                        IATA_training_answer = IATA_training_answer_record.value
                        data.IATA_training_answer= IATA_training_answer
                    else:
                        data.IATA_training_answer = None
                        
    
            # for getting Cr Professional Experience docs
            cr_prof_exp_details=db.query(Cr_Professional_Experience).filter(Cr_Professional_Experience.cr_general_id == cr_id).all()
            # if cr_prof_exp_details:
            #     for pro_exp in cr_prof_exp_details:
            #         if pro_exp.institution_department:
            #             institution_record = db.query(Institution).filter(Institution.institution_id==pro_exp.institution_department).first()
            #             institution_department_name = institution_record.institution_name
            #             pro_exp.institution_department_name = institution_department_name
            #         else:
            #             pro_exp.institution_department_name = None
            
            
            # for getting Cr License Ense docs
            cr_license_ense_details=db.query(Cr_License_Ense).filter(Cr_License_Ense.cr_general_id == cr_id).all()
            if cr_license_ense_details:
                for cr_license in cr_license_ense_details:
                    if cr_license.type_of_license:
                        license_type_record = db.query(LicenseType).filter(LicenseType.license_type_id==cr_license.type_of_license).first()
                        license_type_name = license_type_record.license_type
                        cr_license.license_type_name = license_type_name
                    else:
                        cr_license.license_type_name = None
                                
                    if cr_license.state_region:
                        state_region_record = db.query(CountryDetails).filter(CountryDetails.country_id==cr_license.state_region).first()
                        state_region_answer = state_region_record.region
                        cr_license.state_region_answer = state_region_answer
                    else:
                        cr_license.state_region_answer = None
                                          
                    if  cr_license.country:
                        country_details_record = db.query(CountryDetails).filter(CountryDetails.country_id==cr_license.country).first()
                        country_details_answer = country_details_record.country_name
                        cr_license.country_details_answer = country_details_answer
                    else:
                        cr_license.country_details_answer = None
                        
            
            # for getting Cr Gcp Trai docs
            cr_gcp_trai_details=db.query(Cr_Gcp_Trai).filter(Cr_Gcp_Trai.cr_general_id == cr_id).all()
            if cr_gcp_trai_details:
                for gcp_trail in cr_gcp_trai_details:
                    if gcp_trail.status:
                        gcp_status_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id== gcp_trail.status).first()
                        gcp_status = gcp_status_record.value
                        gcp_trail.gcp_status = gcp_status
                    else:
                        gcp_trail.gcp_status = None
                        
                                
            
            # for getting Cr Specialities docs
            cr_specialities_details=db.query(Cr_Specialities).filter(Cr_Specialities.cr_general_id == cr_id).all()
            # cr_specialities_record = db.query(Cr_Specialities).filter(Cr_Specialities.cr_res_exp_check_list_id==data.cr_res_exp_check_list_id).all()
            if cr_specialities_details:
                for spec in cr_specialities_details:
                    if spec.specialities:
                        specialities_record = db.query(Speciality).filter(Speciality.id== spec.specialities).first()
                        specialities_answer = specialities_record.speciality
                        spec.specialities_answer =specialities_answer
                    else:
                        spec.specialities_answer = None
                                
                    if spec.sub_specialities:
                        sub_specialities_record = db.query(SpecialitySubspeciality).filter(SpecialitySubspeciality.id== spec.sub_specialities).first()
                        sub_specialities_answer = sub_specialities_record.subspeciality
                        spec.sub_specialities_answer =sub_specialities_answer
                    else:
                        spec.sub_specialities_answer = None 
            
                    

            
            # for getting Cr Total Clinical Research Exp docs
            cr_Clinical_Research_Exp_details=db.query(Cr_Total_Clinical_Research_Exp).filter(Cr_Total_Clinical_Research_Exp.cr_general_id == cr_id).all()
            if cr_Clinical_Research_Exp_details:
                for  clinical_exp in cr_Clinical_Research_Exp_details:        
                    if clinical_exp.total_therapeutic_area:
                        total_therapeutic_area_record = db.query(Icd).filter(Icd.icd_id== clinical_exp.total_therapeutic_area).first()
                        total_therapeutic_area_answer = total_therapeutic_area_record.description
                        clinical_exp.total_therapeutic_area_answer =total_therapeutic_area_answer 
                    else:
                        clinical_exp.total_therapeutic_area_answer = None 
                            
                            
                    if clinical_exp.total_sub_therapeutic_area:
                        total_sub_therapeutic_area_record = db.query(Icd).filter(Icd.icd_id== clinical_exp.total_sub_therapeutic_area).first()
                        total_sub_therapeutic_area_answer = total_sub_therapeutic_area_record.description
                        clinical_exp.total_sub_therapeutic_area_answer =total_sub_therapeutic_area_answer
                    else:
                        clinical_exp.total_sub_therapeutic_area_answer = None
                            
                            
                    if clinical_exp.status:
                        clinical_research_status_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id== clinical_exp.status).first()
                        clinical_status = clinical_research_status_record.value
                        clinical_exp.clinical_status =clinical_status
                    else:
                        clinical_exp.clinical_status = None
            




            affiliations = db.execute(query1)
            affiliations_details = affiliations.fetchall()

            cr_docs['education_details']= education_details
            cr_docs['affiliations_details']= affiliations_details
            cr_docs['total_cr_checklist']= cr_checklist
            cr_docs['cr_prof_exp_details']= cr_prof_exp_details
            cr_docs['cr_license_ense_details']= cr_license_ense_details
            cr_docs['cr_gcp_trai_details']= cr_gcp_trai_details
            # cr_docs['cr_specialities_details']= cr_specialities_details
            cr_docs['cr_Clinical_Research_Exp_details']= cr_Clinical_Research_Exp_details
            # print(cr_docs)
            return cr_docs
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def post_cr_doc_details(self,data):
        db = next(get_db())
        try:
            screen_name = "Clinical Researcher"
            # save education details
            studies_label_name = "Education"
            cr_education_list=[]
            for doc in data.education_details:
                cr_education = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = studies_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_education_list.append(cr_education)
            db.add_all(cr_education_list)
            db.commit()
                
            # save education details
            Affiliations_label_name = "Facilities Affiliations"
            cr_affiliations_list=[]
            for doc in data.affiliations_details:
                cr_affiliations = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Affiliations_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_affiliations_list.append(cr_affiliations)
            db.add_all(cr_affiliations_list)
            db.commit()

            # save Professional Details 
            Professional_label_name = "Professional Experience"
            cr_professional_list=[]
            for doc in data.cr_prof_exp_details:
                cr_professional = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Professional_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_professional_list.append(cr_professional)
            db.add_all(cr_professional_list)
            db.commit()

            # save Licenses / ENSE Details 
            Licenses_label_name = "Licenses / ENSE"
            cr_licenses_list=[]
            for doc in data.cr_license_ense_details:
                cr_licenses = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Licenses_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_licenses_list.append(cr_licenses)
            db.add_all(cr_licenses_list)
            db.commit()


                # save GCP Trai Details 
            gcp_label_name = "GCP Trai"
            cr_gcp_list=[]
            for doc in data.cr_gcp_trai_details:
                cr_gcp = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = gcp_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_gcp_list.append(cr_gcp)
            db.add_all(cr_gcp_list)
            db.commit()


                # save Research Experience Details 
            Research_Exp_label_name = "Research Experience"
            cr_research_exp_list=[]
            for doc in data.cr_Clinical_Research_Exp_details:
                cr_research_exp = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Research_Exp_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_research_exp_list.append(cr_research_exp)
            db.add_all(cr_research_exp_list)
            db.commit()


                # save Specialities / Sub-Specialities Details 
            # Sp_subsp_label_name = "Specialities / Sub-Specialities"
            # cr_sp_subsp_list=[]
            # for doc in data.cr_license_ense_details:
            #     cr_sp_subsp = Upload_Documents(
            #             site_id = data.site_id,
            #             cr_code = data.cr_code,
            #             screen_type_name = screen_name,
            #             screen_label_name = Sp_subsp_label_name,
            #             document_name = doc.document_name,
            #             document_attached = doc.document_attached,
            #             version = doc.version,
            #             status = doc.status,
            #             remarks = doc.remarks,
            #             attachment = doc.attachment,
            #             created_by_id = data.created_by_id,
            #             created=datetime.now()
            #         )
            #     cr_sp_subsp_list.append(cr_sp_subsp)
            # db.add_all(cr_sp_subsp_list)
            # db.commit()


                # save Research Experience / Study Type Details 
            study_type_label_name = "Research Experience / Study Type"
            study_type_list=[]
            for doc in data.cr_license_ense_details:
                cr_study_type = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = study_type_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created = datetime.now()
                    )
                study_type_list.append(cr_study_type)
            db.add_all(study_type_list)
            db.commit()

                # save Research Experience / Clinical Study Phases Details 
            study_phases_label_name = "Research Experience / Clinical Study Phases"
            cr_study_phases_list=[]
            for doc in data.cr_license_ense_details:
                cr_study_phases = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = study_phases_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_study_phases_list.append(cr_study_phases)
            db.add_all(cr_study_phases_list)
            db.commit()


               # Check List speciality_cie10
            Checklist_label_name = "Check List"
            cr_checklist_list=[]
            for doc in data.speciality_cie10:
                cr_checklist = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Checklist_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_checklist_list.append(cr_checklist)
            db.add_all(cr_checklist_list)
            db.commit()


               # Check List cv
            cr_cv_list=[]
            for doc in data.cv:
                cr_cv = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Checklist_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_cv_list.append(cr_cv)
            db.add_all(cr_cv_list)
            db.commit()


                # Check List scanned_id
            cr_scanned_id_list=[]
            for doc in data.scanned_id:
                cr_scanned_id = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Checklist_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_scanned_id_list.append(cr_scanned_id)
            db.add_all(cr_scanned_id_list)
            db.commit()


                # Check List scanned_title
            cr_scanned_title_list=[]
            for doc in data.scanned_title:
                cr_scanned_title = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Checklist_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_scanned_title_list.append(cr_scanned_title)
            db.add_all(cr_scanned_title_list)
            db.commit()

                # Check List scanned_license
            cr_scanned_license_list=[]
            for doc in data.scanned_license:
                cr_scanned_license = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Checklist_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_scanned_license_list.append(cr_scanned_license)
            db.add_all(cr_scanned_license_list)
            db.commit()

                # Check List IATA_training
            cr_IATA_training_list=[]
            for doc in data.scanned_title:
                cr_IATA_training = Upload_Documents(
                        site_id = data.site_id,
                        cr_code = data.cr_code,
                        screen_type_name = screen_name,
                        screen_label_name = Checklist_label_name,
                        document_name = doc.document_name,
                        document_attached = doc.document_attached,
                        version = doc.version,
                        status = doc.status,
                        remarks = doc.remarks,
                        attachment = doc.attachment,
                        created_by_id = data.created_by_id,
                        created=datetime.now()
                    )
                cr_IATA_training_list.append(cr_IATA_training)
            db.add_all(cr_IATA_training_list)
            db.commit()

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    # def get_cr_doc_View(self,cr_id):
    #     db = next(get_db())
    #     try:
    #         result= db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr_id,Upload_Documents.screen_type_name == "Clinical Researcher").all()
    #         if result:
    #             return result
    #         else:
    #             return []
    #     except Exception as e:
    #         db.rollback()
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #     finally:
    #         db.close()  
    def get_cr_doc_View(self, cr_id):
        db = next(get_db())
        try:
            results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr_id, Upload_Documents.screen_type_name == "Clinical Researcher").order_by(desc(Upload_Documents.created)).all()

            # Create a dictionary to group documents by document_name
            document_dict = {}
            for result in results:
                document_name = result.document_name
                if document_name not in document_dict:
                    document_dict[document_name] = {
                        "site_id": result.site_id,
                        "cr_id": result.cr_code,
                        "screen_label_name": result.screen_label_name,
                        "document_name": document_name,
                        "document_attached": result.document_attached,
                        # "status": result.status,
                        "remarks": result.remarks,
                        "versions": []
                    }
                document_dict[document_name]["versions"].append({
                    "upload_document_id": result.upload_document_id,
                    "version": result.version,
                    "attachment": result.attachment,
                    "status": result.status
                })

            # Convert the dictionary values to a list
            grouped_results = list(document_dict.values())

            if grouped_results:
                return grouped_results
            else:
                return []
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

         
         
            
    def put_cr_doc_details(self,data):
        db = next(get_db())
        try:
            screen_name = "Clinical Researcher"
            # save education details
            studies_label_name = "Education"
            
            site_id = data.site_id
            cr_code = data.cr_code
            created_by_id = data.created_by_id
            
            
            cr_education_list=[]
            for doc in data.education_details:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                # return upload_document_id
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(education_details), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:
                        
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                        
                        cr_education = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = studies_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_education_list.append(cr_education)
            db.add_all(cr_education_list)
            db.commit()
                
            # save education details
            Affiliations_label_name = "Facilities Affiliations"
            cr_affiliations_list=[]
            for doc in data.affiliations_details:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(affiliations_details), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                        
                        cr_affiliations = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Affiliations_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_affiliations_list.append(cr_affiliations)
            db.add_all(cr_affiliations_list)
            db.commit()

            # save Professional Details 
            Professional_label_name = "Professional Experience"
            cr_professional_list=[]
            for doc in data.cr_prof_exp_details:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_professional_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                        cr_professional = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Professional_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_professional_list.append(cr_professional)
            db.add_all(cr_professional_list)
            db.commit()

            # # save Licenses / ENSE Details 
            Licenses_label_name = "Licenses / ENSE"
            cr_licenses_list=[]
            for doc in data.cr_license_ense_details:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_licenses_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                        cr_licenses = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Licenses_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_licenses_list.append(cr_licenses)
            db.add_all(cr_licenses_list)
            db.commit()


                # save GCP Trai Details 
            gcp_label_name = "GCP Trai"
            cr_gcp_list=[]
            for doc in data.cr_gcp_trai_details:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_gcp_trai_details), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                        cr_gcp = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = gcp_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_gcp_list.append(cr_gcp)
            db.add_all(cr_gcp_list)
            db.commit()


                # save Research Experience Details 



                # save Specialities / Sub-Specialities Details 
            # Sp_subsp_label_name = "Specialities / Sub-Specialities"
            # cr_sp_subsp_list=[]
            # for doc in data.cr_specialities_details:
            #     upload_document_id = doc.upload_document_id
            #     if upload_document_id:
            #         existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
            #         if existing_upload_document_list:
            #             document_attached = doc.document_attached
            #             document_attached = int(document_attached)
            #             # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
            #             existing_upload_document_list.document_name = doc.document_name
            #             existing_upload_document_list.document_attached = document_attached
            #             existing_upload_document_list.version = doc.version
            #             existing_upload_document_list.status = doc.status
            #             existing_upload_document_list.remarks = doc.remarks
            #             existing_upload_document_list.attachment = doc.attachment
            #             existing_upload_document_list.updated_by_id = created_by_id
            #             db.commit()
            #         else:
            #             return f"upload_document_id={upload_document_id} is invalid(cr_sp_subsp_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
            #     else:   
            #         document_attached = doc.document_attached
            #         document_attached = int(document_attached)
            #         cr_sp_subsp = Upload_Documents(
            #                 site_id = data.site_id,
            #                 cr_code = data.cr_code,
            #                 screen_type_name = screen_name,
            #                 screen_label_name = Sp_subsp_label_name,
            #                 document_name = doc.document_name,
            #                 document_attached = document_attached,
            #                 version = doc.version,
            #                 status = doc.status,
            #                 remarks = doc.remarks,
            #                 attachment = doc.attachment,
            #                 created_by_id = data.created_by_id,
            #                 created=datetime.now()
            #             )
            #         cr_sp_subsp_list.append(cr_sp_subsp)
            # db.add_all(cr_sp_subsp_list)
            # db.commit()




            Research_Exp_label_name = "Research Experience"
            cr_research_exp_list=[]
            for doc in data.cr_Clinical_Research_Exp_details:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_research_exp_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
    
                        cr_research_exp = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Research_Exp_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_research_exp_list.append(cr_research_exp)
            db.add_all(cr_research_exp_list)
            db.commit()
            # save Research Experience / Study Type Details 
            study_type_label_name = "Research Experience / Study Type"
            study_type_list=[]
            for doc in data.study_type:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(study_type_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                    
                        cr_study_type = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = study_type_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created = datetime.now()
                            )
                        study_type_list.append(cr_study_type)
            db.add_all(study_type_list)
            db.commit()

            # save Research Experience / Clinical Study Phases Details 
            study_phases_label_name = "Research Experience / Clinical Study Phases"
            cr_study_phases_list=[]
            for doc in data.clinical_study_phases:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_study_phases_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                        cr_study_phases = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = study_phases_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_study_phases_list.append(cr_study_phases)
            db.add_all(cr_study_phases_list)
            db.commit()


            # Check List speciality_cie10
            Checklist_label_name = "Check List"
            cr_checklist_list=[]
            for doc in data.speciality_cie10:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_checklist_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
        
                        cr_checklist = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Checklist_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_checklist_list.append(cr_checklist)
            db.add_all(cr_checklist_list)
            db.commit()


            # Check List cv
            cr_cv_list=[]
            for doc in data.cv:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    
                    if upload_document_id:
                        
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_cv_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:  
                        document_attached = doc.document_attached
                        document_attached = int(document_attached) 
        
                        cr_cv = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Checklist_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_cv_list.append(cr_cv)
            db.add_all(cr_cv_list)
            db.commit()


            # Check List scanned_id
            cr_scanned_id_list=[]
            for doc in data.scanned_id:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_scanned_id_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
        
                        cr_scanned_id = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Checklist_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_scanned_id_list.append(cr_scanned_id)
            db.add_all(cr_scanned_id_list)
            db.commit()


            # Check List scanned_title
            cr_scanned_title_list=[]
            for doc in data.scanned_title:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_scanned_title_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                        cr_scanned_title = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Checklist_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_scanned_title_list.append(cr_scanned_title)
            db.add_all(cr_scanned_title_list)
            db.commit()

            # Check List scanned_license
            cr_scanned_license_list=[]
            for doc in data.scanned_license:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_scanned_license_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                    
                        cr_scanned_license = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Checklist_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_scanned_license_list.append(cr_scanned_license)
            db.add_all(cr_scanned_license_list)
            db.commit()

            # Check List IATA_training
            cr_IATA_training_list=[]
            for doc in data.IATA_training:
                for version in doc.versions:
                    upload_document_id = version.upload_document_id
                    
                    if upload_document_id:
                        existing_upload_document_list = db.query(Upload_Documents).get(upload_document_id)
                        if existing_upload_document_list:
                            document_attached = doc.document_attached
                            document_attached = int(document_attached)
                            # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                            existing_upload_document_list.document_name = doc.document_name
                            existing_upload_document_list.document_attached = document_attached
                            existing_upload_document_list.version = version.version
                            existing_upload_document_list.status = version.status
                            existing_upload_document_list.remarks = doc.remarks
                            existing_upload_document_list.attachment = version.attachment
                            existing_upload_document_list.updated_by_id = created_by_id
                            db.commit()
                        else:
                            return f"upload_document_id={upload_document_id} is invalid(cr_IATA_training_list), Please pass 0 to add new record to db or send appropriate id to edit the same record"    
                    else:   
                        document_attached = doc.document_attached
                        document_attached = int(document_attached)
                        cr_IATA_training = Upload_Documents(
                                site_id = data.site_id,
                                cr_code = data.cr_code,
                                screen_type_name = screen_name,
                                screen_label_name = Checklist_label_name,
                                document_name = doc.document_name,
                                document_attached = document_attached,
                                version = version.version,
                                status = version.status,
                                remarks = doc.remarks,
                                attachment = version.attachment,
                                created_by_id = data.created_by_id,
                                created=datetime.now()
                            )
                        cr_IATA_training_list.append(cr_IATA_training)
            db.add_all(cr_IATA_training_list)
            db.commit()

            is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
            no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
            no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == data.cr_code,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
            cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == data.cr_code,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

            results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == data.cr_code, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

            # Create a dictionary to group documents by document_name
            final_result = []
            if(results):
                document_dict = {}
                for result in results:
                    document_name = result.document_name
                    if document_name not in document_dict:
                        document_dict[document_name] = {
                            "site_id": result.site_id,
                            "cr_id": result.cr_code,
                            "screen_label_name": result.screen_label_name,
                            "document_name": document_name,
                            "document_attached": result.document_attached,
                            # "status": result.status,
                            "remarks": result.remarks,
                            "versions": []
                        }
                    document_dict[document_name]["versions"].append({
                        "upload_document_id": result.upload_document_id,
                        "version": result.version,
                        "attachment": result.attachment,
                        "status": result.status,
                        "created": result.created
                    })

                # Convert the dictionary values to a list
                grouped_results = list(document_dict.values())


                latest_version_dict = {}

    # Iterate through the grouped_results and update the latest version
                for item in grouped_results:
                    document_name = item["document_name"]
                    version_list = item["versions"]
                    
                    # Sort the version list by created timestamp in descending order
                    version_list.sort(key=lambda x: x["created"], reverse=True)
                    
                    # Get the latest version
                    latest_version = version_list[0]["version"]
                    
                    # Update the latest version in the dictionary
                    latest_version_dict[document_name] = latest_version

                # Create a list of objects with the latest version and created timestamp
                # final_result = []

                for item in grouped_results:
                    document_name = item["document_name"]
                    
                    # Check if the document_name is in the latest_version_dict
                    if document_name in latest_version_dict:
                        latest_version = latest_version_dict[document_name]
                        
                        # Find the version with the latest version
                        for version in item["versions"]:
                            if version["version"] == latest_version:
                                # Create a new object with the required fields
                                latest_version_item = {
                                    "site_id": item["site_id"],
                                    "cr_id": item["cr_id"],
                                    "screen_label_name": item["screen_label_name"],
                                    "document_name": item["document_name"],
                                    "document_attached": item["document_attached"],
                                    "remarks": item["remarks"],
                                    "upload_document_id": version["upload_document_id"],
                                    "version": version["version"],
                                    "status": version["status"],
                                    "created": version["created"]
                                }
                                final_result.append(latest_version_item)


            # return cr_documents
            if final_result:

                org_id = db.query(User).filter(User.id == data.created_by_id).first()
                users = db.query(User).filter(User.org_id == org_id.org_id).all()
                pending_document_list = []
                for user in users:
                    document_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                    if(document_status):
                        pending_document_list.extend(document_status)
                pending_document_obj = None        
                for document in pending_document_list:
                    if document.document_status_description.lower() == "pending document":
                        pending_document_obj = document
                        break 
                
                pending_verification_list = []
                for user in users:
                    document_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                    if(document_status):
                        pending_verification_list.extend(document_status)
                pending_verification_obj = None        
                for document in pending_verification_list:
                    if document.document_status_description.lower() == "pending verification":
                        pending_verification_obj = document
                        break 

                approved_document_list = []
                for user in users:
                    document_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                    if(document_status):
                        approved_document_list.extend(document_status)
                approved_document_obj = None        
                for document in approved_document_list:
                    if document.document_status_description.lower() == "approved":
                        approved_document_obj = document
                        break      

                rejected_document_list = []
                for user in users:
                    document_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                    if(document_status):
                        rejected_document_list.extend(document_status)
                rejected_document_obj = None        
                for document in rejected_document_list:
                    if document.document_status_description.lower() == "rejected":
                        rejected_document_obj = document
                        break    

                # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                documents_list = []
                for document in final_result:
                    documents_list.append(document['status'])

                document_status = None  
                if(approved_document_obj and rejected_document_obj and pending_verification_obj):
                    if all(status is None or status == pending_verification_obj.documentstatus_id for status in documents_list):
                        document_status = "Review Pending"
                    elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                        document_status = "Inactive"
                    elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                        document_status = "Rejected"
                    elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                        document_status = "Review Pending" 

                cr_status_list = []
                for user in users:
                    all_cr_status = db.query(Cr_Status).filter(Cr_Status.created_by_id == user.id).all()
                    if(all_cr_status):
                        cr_status_list.extend(all_cr_status)
                cr_status_obj = None        
                for status in cr_status_list:
                    if status.cr_status.lower() == document_status.lower():
                        cr_status_obj = status
                        break 

                status_id = db.query(Cr_Status).filter(func.lower(Cr_Status.cr_status) == document_status.lower()).first()
                cr = db.query(General).filter(General.cr_general_id == data.cr_code).first()
                if(cr):
                    if(cr_status_obj):
                        cr.cr_status = cr_status_obj.cr_status_id
                        db.commit()

            elif no_cr_documents:
                org_id = db.query(User).filter(User.id == data.created_by_id).first()
                users = db.query(User).filter(User.org_id == org_id.org_id).all()
                cr_status_list = []
                for user in users:
                    all_cr_status = db.query(Cr_Status).filter(Cr_Status.created_by_id == user.id).all()
                    if(all_cr_status):
                        cr_status_list.extend(all_cr_status)
                cr_status_obj = None        
                for status in cr_status_list:
                    if status.cr_status.lower() == "review pending":
                        cr_status_obj = status
                        break 
                
                pending_status_id = db.query(Cr_Status).filter(func.lower(Cr_Status.cr_status) == "review pending").first()
                cr = db.query(General).filter(General.cr_general_id == data.cr_code).first()
                if(cr):
                    if(cr_status_obj):
                        cr.cr_status = cr_status_obj.cr_status_id
                        db.commit()

            else:
                org_id = db.query(User).filter(User.id == data.created_by_id).first()
                users = db.query(User).filter(User.org_id == org_id.org_id).all()
                cr_status_list = []
                for user in users:
                    all_cr_status = db.query(Cr_Status).filter(Cr_Status.created_by_id == user.id).all()
                    if(all_cr_status):
                        cr_status_list.extend(all_cr_status)
                cr_status_obj = None        
                for status in cr_status_list:
                    if status.cr_status.lower() == "created":
                        cr_status_obj = status
                        break 

                status_id = db.query(Cr_Status).filter(func.lower(Cr_Status.cr_status) == "created").first()
                cr = db.query(General).filter(General.cr_general_id == data.cr_code).first()
                if(cr):
                    if(cr_status_obj):
                        cr.cr_status = cr_status_obj.cr_status_id
                        db.commit()
            
            return "details added"
            # return final_result
            
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()    

    def get_uploaded_document(self,id):
        db = next(get_db())
        try:
            document = db.query(Upload_Documents).filter(Upload_Documents.upload_document_id == id).first()
            return document
        finally:
            db.close()    