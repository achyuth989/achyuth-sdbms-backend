from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func,desc,asc
from sqlalchemy import or_
from fastapi.responses import JSONResponse  # Import JSONResponse
from app.model.user import User
from app.model.organizations import Organizations
from app.model.site import Site
from app.model.general import General
from app.model.cr_status import Cr_Status
from app.model.questionnaire import Questionnaire
from app.model.rec_population_grp import Rec_Population_grp

from app.model.site_assess_registration import Site_Assess_Registration
from app.model.site_asmt_infrastructure import SiteAsmtInfrastructure
from app.model.legal import Legal
from app.model.site_assess_review import Site_Assess_Review
from app.model.siteassement_orgpersonal import Orgpersonal
from app.model.quality_systems import QualitySystems

from app.model.icd_siterecgonization import Siteicd
from app.model.icd import Icd
from app.model.country_state_muni_trn import CountryStateMuniTrn
from app.model.country_state_muni import CountryStateMuni
from app.model.country_state import CountryState
from app.model.country_details import CountryDetails
from app.model.state import State


class Dashboard:
    def get_dashboard_data(self,user_id):
        db = next(get_db())
        # does user exists
        # we will get user_id from frontend
        # To which organisation he is related to ??(check users table, each user has org_id)
        # then get all users for this organisation(from users table)
        # then get all sites created by these users
        # then get list of cr's for each site
        # Then get respective data
        
        # now get site_code, site_assmt_status, first_time_visits, follow_up_visits
        
        try:
            does_user_exists = db.query(User).filter(User.id ==user_id).first()
            
            if does_user_exists:
                
                # global decarations
                active_data =db.query(Cr_Status).filter(func.lower(func.trim(Cr_Status.cr_status))== "active").first()
                inactive_data = db.query(Cr_Status).filter(func.lower(func.trim(Cr_Status.cr_status))== "inactive").first()
                withdrawn_data = db.query(Cr_Status).filter(func.lower(func.trim(Cr_Status.cr_status))== "withdrawn").first()
                
                if active_data:
                    active_id = active_data.cr_status_id
                else:
                    active_id = None
    
                
                if inactive_data:
                    inactive_id =inactive_data.cr_status_id
                else:
                    inactive_id = None
                
                if withdrawn_data:
                    withdrawn_id = withdrawn_data.cr_status_id
                else:
                    withdrawn_id = None
                
                
                first_question = "Number of First-Time Outpatient Consultations Per Year"
                first_question =first_question.lower().strip()
                        
                annual_question ="Number of Annual Follow-up Outpatient Consultations"
                annual_question = annual_question.lower().strip()
                
                patients_question = "Population Attached to the Site/Institution"
                patients_question = patients_question.lower().strip()
                
                first_question_data = db.query(Questionnaire).filter(func.lower(func.trim(Questionnaire.question))== first_question).first()
                annual_question_data = db.query(Questionnaire).filter(func.lower(func.trim(Questionnaire.question))== annual_question).first()
                patients_question_data = db.query(Questionnaire).filter(func.lower(func.trim(Questionnaire.question))== patients_question).first()
                
                if first_question_data:     
                    first_question_id =first_question_data.questionnaire_id
                else: 
                    first_question_id = None
                
                if annual_question_data:
                    annual_question_id = annual_question_data.questionnaire_id
                else:
                    annual_question_id = None
                    
                if patients_question_data:
                    patients_question_id = patients_question_data.questionnaire_id
                else:
                    patients_question_id = None
                
                
                # get org_id from user
                org_id_of_this_user = does_user_exists.org_id
                
                if org_id_of_this_user:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== org_id_of_this_user).all()
                    
                    
                    # ---------side widget starts from here------------------------------------------------------
                    # total_cr_count
                    sites_list=[]
                    for users in list_of_users_related_to_org:
                        site = db.query(Site).filter(Site.created_by_id == users.id).all()
                        if site:
                            sites_list.extend(site)
                    all_sites_count = len(sites_list)
                    # get_list_of_sites_related_to_org = 
                    # active_sites_list =[]
                    cr_list = []

                    for site in sites_list:
                        # if site.status == active_id:
                        #     active_sites_list.append(site)
                            
                        cr_gen = db.query(General).filter(General.site_id == site.site_id).filter(or_(General.cr_status == active_id,General.cr_status == inactive_id, General.cr_status == withdrawn_id)).all()
                        if cr_gen:
                            cr_list.extend(cr_gen)
                        
                    # active_sites_count = len(active_sites_list)   
                    cr_list_count = len(cr_list)
                    # total_cr_count
                    
                    # First-Time Outpatient Consultations Per Year
                    first_sum = 0
                    annual_sum = 0
                    patients_sum = 0
                    for population in sites_list:
                        
                        first_record = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == population.site_id).filter(Rec_Population_grp.question == first_question_id).first()
                        if first_record:
                            if first_record.input is not None:
                                first_input_value = first_record.input
                                first_sum += first_input_value
                        
                        annual_record = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == population.site_id).filter(Rec_Population_grp.question == annual_question_id).first()
                        if annual_record:
                            if annual_record.input is not None:
                                annual_input_value = annual_record.input
                                annual_sum += annual_input_value
                            
                        patients_record = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == population.site_id).filter(Rec_Population_grp.question == patients_question_id).first()
                        if patients_record:
                            if patients_record.input is not None:
                                patients_input_value = patients_record.input
                                patients_sum +=patients_input_value

                    side_widget = {
                        "total_cr_count":cr_list_count,
                        "first_sum":first_sum,
                        "follow_up_sum":annual_sum,
                        "sites":all_sites_count,
                        "patients":patients_sum
                    }
                    # --------------------side_widget ends here----------------------------------------------------
                    
                    # ----------------------------------individual site count starts from here--------------------------------
                    
                    # return sites_list 
                    main_widget =[]
                
                    for site in sites_list:
                        registration = db.query(Site_Assess_Registration).filter(Site_Assess_Registration.site_id == site.site_id).first()
                        infra = db.query(SiteAsmtInfrastructure).filter(SiteAsmtInfrastructure.site_id == site.site_id).first()
                        legal = db.query(Legal).filter(Legal.site_id == site.site_id).first()
                        review = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_id == site.site_id).first()
                        org_personal = db.query(Orgpersonal).filter(Orgpersonal.site_id == site.site_id).first()
                        quality = db.query(QualitySystems).filter(QualitySystems.site_id == site.site_id).first()

                        # status = ""
                        
                        if(registration and infra and legal and review and org_personal and quality):
                            asmt_status = "Completed"
                        elif(registration or infra or legal or review or org_personal or quality):
                            asmt_status = "In Progress"  
                        else:
                            asmt_status = "Not Started"   
                        
                        first_input_value = 0
                        first_record = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == site.site_id).filter(Rec_Population_grp.question == first_question_id).first()
                        if first_record:
                            if first_record.input is not None:
                                first_input_value = first_record.input
                            
                        annual_input_value = 0
                        annual_record = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == site.site_id).filter(Rec_Population_grp.question == annual_question_id).first()
                        if annual_record:
                            if annual_record.input is not None:
                                annual_input_value = annual_record.input
                            
                        
                    
                        cr_gen = db.query(General).filter(General.site_id == site.site_id).filter(or_(General.cr_status == active_id,General.cr_status == inactive_id, General.cr_status == withdrawn_id)).all()
                        if cr_gen:
                            cr_list_count = len(cr_gen)
                        else:
                            cr_list_count = 0
                    
                        site_object = {
                        "site_id": site.site_id,
                        "site_code":site.site_code,
                        "site_name": site.site_name,
                        "status": asmt_status,
                        "first_time_visits":first_input_value,
                        "follow_up_visits":annual_input_value,
                        "cr_count":cr_list_count
                        }
                        main_widget.append(site_object) 
                    # ---------------------------------------site locations code starts from here-----------------------------------------------------
                        
                        # we have siteslist
                        # get state_codes from country_state_mini_trn_id in sites table
                        # the get list of sites mapped to each state_code
                        
                        # sites = country_state_muni_trn_id
                        # country_state_muni_trn = municipality_id
                        # country_state_muni(municipality_id) = country_state_muni_id
                        # country_state_muni = country_state_id
                        # country_state == country_details,state(mapped)
                        # country will county details 
                        # state will have states list
                        # get sites list under each state code
                        
                        # mock object
                        # {
                        # "locations": [
                        #     {
                        #         "state_code": "xxx",
                        #         "sites_count": 3,
                        #         "sites_list": [
                        #             {
                        #              "name": "xx",
                        #               "code":"xx"
                        #             }
                        #         ]
                        #     }
                        # ]
                        # }
                        
                        
                        
                        # commenting this code because created a new separte api for this feature--- 
                        # state_code_for_this_org=set()
                        
                        # for site in sites_list:
                            
                        #     country_state_muni_trn = db.query(CountryStateMuniTrn).filter(CountryStateMuniTrn.country_state_muni_trn_id== site.country_state_muni_trn_id).first()
                            
                        #     country_state_muni = db.query(CountryStateMuni).filter(CountryStateMuni.country_state_muni_id == country_state_muni_trn.municipality_id).first()
                            
                        #     country_state = db.query(CountryState).filter(CountryState.country_state_id == country_state_muni.country_state_id).first()
                            
                        #     state = db.query(State).filter(State.state_id==country_state.state_id).first()
                        #     # need to discuss
                            
                        #     code = state.state_code
                        #     site.state_code = code
                            
                        #     state_code_for_this_org.add(code)
                            
                        # state_code_for_this_org = list(state_code_for_this_org)
                            
                            
                            
                        # state_code_data = []
                        # for code in state_code_for_this_org:
                        #     sites_data =[]
                        #     sites_count = 0
                            
                        #     for site in sites_list:
                        #         if site.state_code == code:
                        #             sites_data.append(
                        #                 {
                        #                     "site_name":site.site_name,
                        #                     "site_code":site.site_code
                        #                 }
                        #             )
                        #             sites_count += 1
                                    
                        #     state_code_data.append({
                        #         "state_code": code,
                        #         "sites_count": sites_count,
                        #         "sites_list": sites_data
                        #     })  

                    
                    combined_data = {
                        "side_widget": side_widget,
                        "main_widget": main_widget 
                    }       
                    
                    return combined_data
                else:
                    # show dummy data
                    return JSONResponse(
                        content={"user_id":f"{user_id} is not mapped to any organisation"},
                        status_code=status.HTTP_404_NOT_FOUND,
                        headers={"Content-Type": "application/json"}  # Set the Content-Type header
                    )  
                    
                 
            else:
                return JSONResponse(
                    content={"user_id":f"{user_id} not found in users table"},
                    status_code=status.HTTP_404_NOT_FOUND,
                    headers={"Content-Type": "application/json"}  # Set the Content-Type header
                )     
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:        
            db.close()
            
            
        # ----------------------------------------------------dashboard map data-------------------------------------------
    def get_dashboard_map_data(self,user_id):
        db = next(get_db())
        try:
            does_user_exists = db.query(User).filter(User.id ==user_id).first()
            
            if does_user_exists:

                # get org_id from user
                org_id_of_this_user = does_user_exists.org_id
                
                if org_id_of_this_user:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== org_id_of_this_user).all()
                    
                    
                    # ---------side widget starts from here------------------------------------------------------
                    # total_cr_count
                    sites_list=[]
                    for users in list_of_users_related_to_org:
                        site = db.query(Site).filter(Site.created_by_id == users.id).all()
                        if site:
                            sites_list.extend(site)
                

                    state_code_for_this_org=set()
                                
                    for site in sites_list:
                        # country_state_muni_trn_id_data =  db.query(Site).filter(Site.country_state_muni_trn_id)
                                    
                        # country_state_muni_trn_id = site.country_state_muni_trn_id
                                    
                        country_state_muni_trn = db.query(CountryStateMuniTrn).filter(CountryStateMuniTrn.country_state_muni_trn_id== site.country_state_muni_trn_id).first()          
                        country_state_muni = db.query(CountryStateMuni).filter(CountryStateMuni.country_state_muni_id == country_state_muni_trn.municipality_id).first()    
                        country_state = db.query(CountryState).filter(CountryState.country_state_id == country_state_muni.country_state_id).first()           
                        state = db.query(State).filter(State.state_id==country_state.state_id).first()
                        # need to discuss
                                    
                        code = state.state_code
                        site.state_code = code
                                    
                        state_code_for_this_org.add(code)
                                    
                    state_code_for_this_org = list(state_code_for_this_org)
                                    
                                    
                                    
                    state_code_data = []
                    for code in state_code_for_this_org:
                        sites_data =[]
                        sites_count = 0
                                    
                        for site in sites_list:
                            if site.state_code == code:
                                sites_data.append(
                                    {
                                        "site_name":site.site_name,
                                        "site_code":site.site_code
                                    }
                                )
                                sites_count += 1
                                            
                        state_code_data.append({
                            "state_code": code,
                            "sites_count": sites_count,
                            "sites_list": sites_data
                        })
                        
                    return state_code_data
                else:
                    # show dummy data
                    return JSONResponse(
                        content={"user_id":f"{user_id} is not mapped to any organisation"},
                        status_code=status.HTTP_404_NOT_FOUND,
                        headers={"Content-Type": "application/json"}  # Set the Content-Type header
                    )  
                    
                    
            else:
                return JSONResponse(
                    content={"user_id":f"{user_id} not found in users table"},
                    status_code=status.HTTP_404_NOT_FOUND,
                    headers={"Content-Type": "application/json"}  # Set the Content-Type header
                )               


            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

     # ----------------------------------------------------dashboard icd data-------------------------------------------
    def get_dashboard_icd_data(self,user_id):
        db = next(get_db())
        try:
            does_user_exists = db.query(User).filter(User.id ==user_id).first()
            
            if does_user_exists:

                # get org_id from user
                org_id_of_this_user = does_user_exists.org_id
                
                if org_id_of_this_user:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== org_id_of_this_user).all()
                    
                    sites_list=[]
                    for users in list_of_users_related_to_org:
                        site = db.query(Site).filter(Site.created_by_id == users.id).all()
                        if site:
                            sites_list.extend(site)
                

                    state_code_for_this_org=set()
 
                    icd = {}
                    for site in sites_list: 
                        site_rec_icd_datas = db.query(Siteicd).filter(Siteicd.site_id == site.site_id).all()
                        for site_rec_icd_data in site_rec_icd_datas:
                            icd_data = db.query(Icd).filter(or_(
                                Icd.icd_id == site_rec_icd_data.top_icd_id,
                                Icd.icd_id == site_rec_icd_data.orphan_icd_id
                            )).first()
                            if icd_data:
                                count = 0
                                if site_rec_icd_data.top_count_of_thread is not None:
                                    count = int(site_rec_icd_data.top_count_of_thread)
                                elif site_rec_icd_data.orphan_count_of_thread is not None:
                                    count = int(site_rec_icd_data.orphan_count_of_thread)
                                else:
                                    count = 0
                                if icd_data.icd_code in icd:
                                    icd[icd_data.icd_code]["count"] += count
                                else:
                                    icd[icd_data.icd_code] = {
                                        "icd_code" : icd_data.icd_code,
                                        "icd_description" : icd_data.description,
                                        "icd_level" : icd_data.icd_level,
                                        "count" : count
                                    }
                    icd_list = list(icd.values())
                    return icd_list
                else:
                    # show dummy data
                    return JSONResponse(
                        content={"user_id":f"{user_id} is not mapped to any organisation"},
                        status_code=status.HTTP_404_NOT_FOUND,
                        headers={"Content-Type": "application/json"}  # Set the Content-Type header
                    )  
                    
                    
            else:
                return JSONResponse(
                    content={"user_id":f"{user_id} not found in users table"},
                    status_code=status.HTTP_404_NOT_FOUND,
                    headers={"Content-Type": "application/json"}  # Set the Content-Type header
                )               


            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()