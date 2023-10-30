from app.model.miscellaneous import Miscellaneous
from app.model.study_phases import StudyPhases
from app.model.research_product import Research_Product
from app.model.study_type import Study_Type
from app.model.cr import Cr
from app.model.institution import Institution
from app.model.license_type import LicenseType
from app.model.country_details import CountryDetails
from app.model.specialities_subspecialities import SpecialitySubspeciality
from app.model.speciality import Speciality
from app.model.icd import Icd
from app.model.cr_professional_experience import Cr_Research_Exp_Check_List,Cr_Professional_Experience,Cr_License_Ense,Cr_Gcp_Trai,Cr_Specialities,Cr_Total_Clinical_Research_Exp
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func,asc
from datetime import datetime
from app.model.general import General


class Cr_Professional_Exp_Service:
    def add_cr_professional_exp_details(self,cr_exp):
        db = next(get_db())
        try:
            # all types of exceptions are handled in this file (post,put,get)
            study_type_array = cr_exp.study_type
            study_type_string =",".join(study_type_array)
            
            study_phase_array = cr_exp.clinical_study_phases
            study_phase_string = ",".join(study_phase_array)
            
            created_by_id = cr_exp.created_by_id
            site_id = cr_exp.site_id
            cr_code = db.query(General).filter(General.cr_code == cr_exp.cr_code).first()
            
            # get primary key of parent table--->Cr_Research_Exp_Check_List
            # existing_cr_res_exp_check_list_id = cr_exp.cr_res_exp_check_list_id sk
            
            
            # assigning existing id as the new_id, we use this id in one case discussed below-->
            # lets say first time user submitted the form with only half details.
            # now user came to the same page trying add new details that he left at first attempt
            # now the question comes to the system what should I do. Do the system perform edit operation or add new record operation.
            # we know it is a new record so the system should add new record.But there is a problem at system stand point.
            # each table is taking the parent primary which is getting generated dynamically while adding a new record. Here the parent is already having the dynamic Id. 
            # Now which id should be passed to the new_record-->either dynamic one or existing one. Yes it should take existing one.
            
            # So there is a situation where you need to take existing id(instead of dynamic id) and pass it to the new record.
            
            # declaring variables globally.(Mandatory)
            
            # if existing_cr_res_exp_check_list_id:sk
            #     new_cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
            # else:
            #     new_cr_exp = None
            #     new_cr_res_exp_check_list_id = None
                
                
            
            if cr_code:
                # editing the existing record
                existing_cr_exp_check_list = db.query(Cr_Research_Exp_Check_List).filter(Cr_Research_Exp_Check_List.cr_res_exp_check_list_id == cr_exp.cr_res_exp_check_list_id).first()
                if existing_cr_exp_check_list:
                    # existing_cr_exp_check_list.site_id = site_id
                    existing_cr_exp_check_list.cr_code = cr_exp.cr_code
                    existing_cr_exp_check_list.study_type = study_type_string
                    existing_cr_exp_check_list.clinical_study_phases = study_phase_string
                    existing_cr_exp_check_list.speciality_cie10 = cr_exp.speciality_cie10
                    existing_cr_exp_check_list.cv = cr_exp.cv
                    existing_cr_exp_check_list.scanned_id = cr_exp.scanned_id
                    existing_cr_exp_check_list.scanned_title = cr_exp.scanned_title
                    existing_cr_exp_check_list.scanned_license = cr_exp.scanned_license
                    existing_cr_exp_check_list.IATA_training = cr_exp.IATA_training
                    existing_cr_exp_check_list.updated_by_id = created_by_id
                    existing_cr_exp_check_list.updated = datetime.now()
                    db.commit()
                # else:
                #     return f"cr_res_exp_check_list_id={cr_exp.cr_res_exp_check_list_id} is invalid(main table), Please pass 0 to add new record to db or send appropriate id to edit the same record"
                else:
                    # adding new record
                    new_cr_exp = Cr_Research_Exp_Check_List(
                        # site_id = site_id,
                        # cr_code = cr_exp.cr_code,
                        cr_general_id = cr_code.cr_general_id,
                        study_type = study_type_string,
                        clinical_study_phases = study_phase_string,
                        speciality_cie10 = cr_exp.speciality_cie10,
                        cv = cr_exp.cv,
                        scanned_id = cr_exp.scanned_id,
                        scanned_title = cr_exp.scanned_title,
                        scanned_license = cr_exp.scanned_license,
                        IATA_training = cr_exp.IATA_training,
                        created_by_id = created_by_id
                    )
                    db.add(new_cr_exp)
                    db.commit()
                    db.refresh(new_cr_exp)
                # return "details added"
            
                # get primary id of Cr_Research_Exp_Check_List(parent)
                # new_cr_res_exp_check_list_id = new_cr_exp.cr_res_exp_check_list_id
          
            

            # professional_certificate
            for prof_exp in cr_exp.professional_certificate:
                # get primary key of professional_certificate for each record
                prof_exp_id = prof_exp.cr_prof_exp_id
                if prof_exp_id:
                    existing_prof_exp = db.query(Cr_Professional_Experience).get(prof_exp_id)
                    # existing_cr_exp_check_list = db.query(Cr_Research_Exp_Check_List).get(existing_cr_res_exp_check_list_id)
                    if existing_prof_exp:
                        # editing the existing record
                        # existing_prof_exp.site_id = site_id
                        # existing_prof_exp.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                        existing_prof_exp.job_title = prof_exp.job_title
                        existing_prof_exp.institution_department = prof_exp.institution_department
                        existing_prof_exp.year_started = prof_exp.year_started
                        existing_prof_exp.year_completed = prof_exp.year_completed
                        existing_prof_exp.updated_by_id = created_by_id
                        # existing_cr_exp_check_list.updated_by_id = created_by_id
                        existing_prof_exp.updated = datetime.now()
                        db.commit()
                    else:
                        return f"cr_prof_exp_id={prof_exp_id} is invalid(professiona exp), Please pass 0 to add new record to db or send appropriate id to edit the same record"
                else:
                    new_prof_exp = Cr_Professional_Experience(
                        # site_id = site_id,
                        # cr_res_exp_check_list_id = new_cr_res_exp_check_list_id,
                        cr_general_id = cr_code.cr_general_id,
                        job_title = prof_exp.job_title,
                        institution_department = prof_exp.institution_department,
                        year_started = prof_exp.year_started,
                        year_completed = prof_exp.year_completed,
                        created_by_id = created_by_id
                    )
                    db.add(new_prof_exp)
                    db.commit()
                    db.refresh(new_prof_exp)
                
            # licenses
            for license_obj in cr_exp.licenses:
                existing_license_id = license_obj.cr_lic_ense_id
                if existing_license_id:
                    existing_license_record = db.query(Cr_License_Ense).get(existing_license_id)
                    # existing_cr_exp_check_list = db.query(Cr_Research_Exp_Check_List).get(existing_cr_res_exp_check_list_id)
                    if existing_license_record:
                        # editing the existing license record
                        # existing_license_record.cr_res_exp_check_list_id = existing_cr_res_exp_check_list_id
                        existing_license_record.type_of_license = license_obj.type_of_license
                        existing_license_record.license_issuer = license_obj.license_issuer
                        existing_license_record.professional_license_number = license_obj.professional_license_number
                        existing_license_record.state_region = license_obj.state_region
                        existing_license_record.country = license_obj.country
                        existing_license_record.issue_date = license_obj.issue_date
                        existing_license_record.expiration_date = license_obj.expiration_date
                        existing_license_record.updated_by_id = created_by_id
                        # existing_cr_exp_check_list.updated_by_id = created_by_id
                        existing_license_record.updated = datetime.now()
                        db.commit()
                    else:
                        return f"cr_lic_ense_id={existing_license_id} is invalid(licenses), Please pass 0 to add new record to db or send appropriate id to edit the same record"
                else:
                    new_license = Cr_License_Ense(
                        cr_general_id = cr_code.cr_general_id,
                        # cr_res_exp_check_list_id= new_cr_res_exp_check_list_id,
                        type_of_license = license_obj.type_of_license,
                        license_issuer = license_obj.license_issuer,
                        professional_license_number = license_obj.professional_license_number,
                        state_region = license_obj.state_region,
                        country = license_obj.country,
                        issue_date = license_obj.issue_date,
                        expiration_date = license_obj.expiration_date,
                        created_by_id = created_by_id
                    )
                    db.add(new_license)
                    db.commit()
                    db.refresh(new_license)
               
               
            # gcp_trails   
            for gcp_obj in cr_exp.gcp_trail:
                existing_gcp_id = gcp_obj.cr_res_exp_id
                if existing_gcp_id:
                    existing_gcp_record = db.query(Cr_Gcp_Trai).get(existing_gcp_id)
                    # existing_cr_exp_check_list = db.query(Cr_Research_Exp_Check_List).get(existing_cr_res_exp_check_list_id)
                    if existing_gcp_record:
                        # editing the existing_gcp_record
                        existing_gcp_record.training_provider = gcp_obj.training_provider
                        existing_gcp_record.title_of_training = gcp_obj.title_of_training
                        existing_gcp_record.version = gcp_obj.version
                        existing_gcp_record.date_completed = gcp_obj.date_completed
                        existing_gcp_record.status = gcp_obj.status
                        existing_gcp_record.updated_by_id = created_by_id
                        # existing_cr_exp_check_list.updated_by_id = created_by_id
                        existing_gcp_record.updated = datetime.now()
                        db.commit()
                    else:
                        return f"cr_res_exp_id = {existing_gcp_id} is invalid(GCP tria). Please pass 0 to add new record to db or send appropriate id to edit the same record"
                else:
                    
                    new_gcp_trial = Cr_Gcp_Trai(
                        cr_general_id = cr_code.cr_general_id,
                        # cr_res_exp_check_list_id = new_cr_res_exp_check_list_id,
                        training_provider = gcp_obj.training_provider,
                        title_of_training = gcp_obj.title_of_training,
                        version = gcp_obj.version,
                        date_completed = gcp_obj.date_completed,
                        status = gcp_obj.status,
                        created_by_id = created_by_id
                    )
                    db.add(new_gcp_trial)
                    db.commit()
                    db.refresh(new_gcp_trial)
                
            # specialities and sub_specialities
            for speciality in cr_exp.specialities:
                existing_cr_theura_area_exp_id = speciality.cr_theura_area_exp_id
                if existing_cr_theura_area_exp_id:
                    existing_cr_speciality_record = db.query(Cr_Specialities).get(existing_cr_theura_area_exp_id)
                    # existing_cr_exp_check_list = db.query(Cr_Research_Exp_Check_List).get(existing_cr_res_exp_check_list_id)
                    if existing_cr_speciality_record:
                        # editing the existing record
                        existing_cr_speciality_record.specialities = speciality.specialities
                        existing_cr_speciality_record.sub_specialities = speciality.sub_specialities
                        existing_cr_speciality_record.updated_by_id = created_by_id
                        # existing_cr_exp_check_list.updated_by_id = created_by_id
                        existing_cr_speciality_record.updated = datetime.now()
                        db.commit()
                    else:
                        return f"cr_theura_area_exp_id = {existing_cr_theura_area_exp_id} is invalid(Cr specialities). Please pass 0 to add new record to db or send appropriate id to edit the same record"
                else:
                    
                    new_specialities = Cr_Specialities(
                        # cr_res_exp_check_list_id = new_cr_res_exp_check_list_id,
                        cr_general_id = cr_code.cr_general_id,
                        specialities = speciality.specialities,
                        sub_specialities = speciality.sub_specialities,
                        created_by_id = created_by_id
                    )
                    db.add(new_specialities)
                    db.commit()
                    db.refresh(new_specialities)
                    
            # total clinical exp
            for clinical_exp_obj in cr_exp.total_clinical_exp:
                existing_cr_tot_cli_res_exp_id = clinical_exp_obj.cr_tot_cli_res_exp_id
                if existing_cr_tot_cli_res_exp_id:
                    existing_total_cli_record = db.query(Cr_Total_Clinical_Research_Exp).get(existing_cr_tot_cli_res_exp_id)
                    # existing_cr_exp_check_list = db.query(Cr_Research_Exp_Check_List).get(existing_cr_res_exp_check_list_id)
                    if existing_total_cli_record:
                        # editing the existing record
                        existing_total_cli_record.total_therapeutic_area = clinical_exp_obj.total_therapeutic_area
                        existing_total_cli_record.total_sub_therapeutic_area = clinical_exp_obj.total_sub_therapeutic_area
                        existing_total_cli_record.sponsor_name = clinical_exp_obj.sponsor_name
                        existing_total_cli_record.cro_name = clinical_exp_obj.cro_name
                        existing_total_cli_record.no_of_completed_studies = clinical_exp_obj.no_of_completed_studies
                        existing_total_cli_record.no_of_ongoing_studies = clinical_exp_obj.no_of_ongoing_studies
                        existing_total_cli_record.start_date = clinical_exp_obj.start_date
                        existing_total_cli_record.end_date = clinical_exp_obj.end_date
                        existing_total_cli_record.status = clinical_exp_obj.status
                        existing_total_cli_record.updated_by_id = created_by_id
                        # existing_cr_exp_check_list.updated_by_id = created_by_id
                        existing_total_cli_record.updated = datetime.now()
                        db.commit()
                    else:
                        return f"cr_tot_cli_res_exp_id = {existing_cr_tot_cli_res_exp_id} is invalid(Cr total_clinical_exp). Please pass 0 to add new record to db or send appropriate id to edit the same record"
                else:
                    
                    new_clinical_exp = Cr_Total_Clinical_Research_Exp(
                        # cr_res_exp_check_list_id = new_cr_res_exp_check_list_id,
                        cr_general_id = cr_code.cr_general_id,
                        total_therapeutic_area = clinical_exp_obj.total_therapeutic_area,
                        total_sub_therapeutic_area = clinical_exp_obj.total_sub_therapeutic_area,
                        sponsor_name = clinical_exp_obj.sponsor_name,
                        cro_name = clinical_exp_obj.cro_name,
                        no_of_completed_studies = clinical_exp_obj.no_of_completed_studies,
                        no_of_ongoing_studies = clinical_exp_obj.no_of_ongoing_studies,
                        start_date = clinical_exp_obj.start_date,
                        end_date = clinical_exp_obj.end_date,
                        status = clinical_exp_obj.status,
                        created_by_id = created_by_id
                    )
                    
                    db.add(new_clinical_exp)
                    db.commit()
                    db.refresh(new_clinical_exp)
                
            return "clinical research experience details added succesfully" 
            
        
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
            
            
            
    def get_cr_professional_exp_details_by_site_id(self,cr_code):
        db = next(get_db())
        try:
            
            cr_research_exp_check_list = db.query(Cr_Research_Exp_Check_List).filter(Cr_Research_Exp_Check_List.cr_general_id == cr_code).all() 
            if cr_research_exp_check_list:
                # professional_certificate =[]
                # licenses = []
                # gcp_trail =[]
                # study_type=[]
                # clinical_study_phases =[]
                # specialities = []
                # total_clinical_exp = []
                
                
                for data in cr_research_exp_check_list:
                    
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
                
                
                    # get professional_experience
                    cr_professional_experience_record = db.query(Cr_Professional_Experience).filter(Cr_Professional_Experience.cr_general_id== cr_code).all()
                    # need to add if else ladder here 
                    if cr_professional_experience_record:
                        # for pro_exp in cr_professional_experience_record:
                        #     if pro_exp.institution_department:
                        #         institution_record = db.query(Institution).filter(Institution.institution_id==pro_exp.institution_department).first()
                        #         institution_department_name = institution_record.institution_name
                        #         pro_exp.institution_department_name = institution_department_name
                        #     else:
                        #         pro_exp.institution_department_name = None
                        data.professional_certificate = cr_professional_experience_record
                    else:
                        data.professional_certificate = []
                      
                      
                    # get license list    
                    cr_license_ense_record = db.query(Cr_License_Ense).filter(Cr_License_Ense.cr_general_id== cr_code).all()
                    if cr_license_ense_record:
                        for cr_license in cr_license_ense_record:
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
                                
                                
                        data.licenses = cr_license_ense_record
                        
                    else:
                        data.licenses = []
                        
                        
                    # get cr_gcp_trai_list
                    cr_gcp_trai_record = db.query(Cr_Gcp_Trai).filter(Cr_Gcp_Trai.cr_general_id== cr_code).all()
                    if cr_gcp_trai_record:
                        for gcp_trail in cr_gcp_trai_record:
                            if gcp_trail.status:
                                gcp_status_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id== gcp_trail.status).first()
                                gcp_status = gcp_status_record.value
                                gcp_trail.gcp_status = gcp_status
                            else:
                                gcp_trail.gcp_status = None
                                
                        data.gcp_trail = cr_gcp_trai_record
                    else:
                        data.gcp_trail = []
                        
                        
                    # get specialities 
                    cr_specialities_record = db.query(Cr_Specialities).filter(Cr_Specialities.cr_general_id==cr_code).all()
                    if cr_specialities_record:
                        for spec in cr_specialities_record:
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
                            
                             
                        data.specialities = cr_specialities_record
                    else:
                        data.specialities = []

                    # get cr_total_clinical_research_exp 
                    cr_total_clinical_research_exp_record = db.query(Cr_Total_Clinical_Research_Exp).filter(Cr_Total_Clinical_Research_Exp.cr_general_id==cr_code).all()
                    if cr_total_clinical_research_exp_record:
                        for  clinical_exp in cr_total_clinical_research_exp_record:
                            
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
                                
                        data.total_clinical_exp = cr_total_clinical_research_exp_record       
                        
                        
                    else:
                        data.total_clinical_exp = []
            
                return cr_research_exp_check_list
                            
                    
                  
                    
                    
                    # clinical_study_phases
                    
                
                
                    # return cr_professional_experience_record
            else:
                return []
                # raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "cr_code doesn't exist.")
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
            
    
            
    def get_all_cr_specialities(self):
        db = next(get_db())
        try:
            
            cr_subspeciality_record = db.query(SpecialitySubspeciality).order_by(asc(SpecialitySubspeciality.id)).all()
            
            for specialities in cr_subspeciality_record:
                speciality_record = db.query(Speciality).filter(Speciality.id == specialities.speciality_id).all()
                for spec in speciality_record:
                    specialities_answer = spec.speciality
                    specialities.speciality = specialities_answer
            return cr_subspeciality_record
                
        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
        
    def delete_cr_professional_by_site_id_and_primary_id(self,primary_key,parameter):  
        db = next(get_db()) 
        try:
            # parameters = pro_exp,licenses,gcp,spec,total_exp
            
            parameter = parameter.lower()
            if parameter == "prof_exp":
                prof_exp_site_details = db.query(Cr_Professional_Experience).filter(Cr_Professional_Experience.cr_prof_exp_id == primary_key).first()
                if prof_exp_site_details:
                    db.delete(prof_exp_site_details)
                    db.commit()
                    return "prof_exp_details deleted successfully"
                else:
                    return f"cr_prof_exp_id={primary_key} is invalid"
                
            elif parameter == "licenses":
                licenses_details = db.query(Cr_License_Ense).filter(Cr_License_Ense.cr_lic_ense_id == primary_key).first()
                if licenses_details:
                    db.delete(licenses_details)
                    db.commit()
                    return "licenses_details deleted successfully"
                else:
                    return f"cr_lic_ense_id={primary_key} is invalid"

            elif parameter == "gcp":
                gcp_details = db.query(Cr_Gcp_Trai).filter(Cr_Gcp_Trai.cr_res_exp_id == primary_key).first()
                if gcp_details:
                    db.delete(gcp_details)
                    db.commit()
                    return "gcp_details deleted successfully"
                else:
                    return f"cr_res_exp_id={primary_key} is invalid"
                
            elif parameter == "spec":
                spec_details = db.query(Cr_Specialities).filter(Cr_Specialities.cr_theura_area_exp_id == primary_key).first()
                if spec_details:
                    db.delete(spec_details)
                    db.commit()
                    return "spec_details deleted successfully"
                else:
                    return f"cr_theura_area_exp_id={primary_key} is invalid"
            elif parameter == "total_exp":
                total_exp_details = db.query(Cr_Total_Clinical_Research_Exp).filter(Cr_Total_Clinical_Research_Exp.cr_tot_cli_res_exp_id == primary_key).first()
                if total_exp_details:
                    db.delete(total_exp_details)
                    db.commit()
                    return "total_exp_details deleted successfully"
                else:
                    return f"cr_tot_cli_res_exp_id={primary_key} is invalid"
            else:
                return f"parameter={parameter} is invalid"
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()