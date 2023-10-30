from app.model.site import Site
from app.model.site_assess_registration import Site_Assess_Registration
from app.model.site_asmt_infrastructure import SiteAsmtInfrastructure
from app.model.legal import Legal
from app.model.site_assess_review import Site_Assess_Review
from app.model.siteassement_orgpersonal import Orgpersonal
from app.model.quality_systems import QualitySystems
from app.model.miscellaneous import Miscellaneous
from app.model.rec_population_grp import Rec_Population_grp
from app.model.icd_siterecgonization import Siteicd
from app.model.site_rec_hospital_infra import SiteRecHospitalInfra
from app.model.cr_infra_site_rec import Cr_infra
from app.model.it import It
from app.model.site_rec_hr  import Siterec_hr
from app.model.cr import Cr
from app.model.regulatory_info_site_rec import RegulatoryInfo
from app.model.general import General
from app.model.cr_gen_facilities_affiliations import GeneralAffiliations
from app.model.cr_gen_education import GeneralEducation
from app.model.cr_professional_experience import Cr_Research_Exp_Check_List, Cr_Professional_Experience, Cr_License_Ense, Cr_Gcp_Trai, Cr_Specialities, Cr_Total_Clinical_Research_Exp 
from app.model.user import User
from app.model.organizations import Organizations
from app.model.upload_documents import Upload_Documents



from app.model.document_status import Document_Status
from app.model.upload_documents import Upload_Documents

from app.db.database import get_db
from fastapi import HTTPException, status
from sqlalchemy import and_ , func, desc

class Site_Recognition:
    def sites_rec_list(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]  
        active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
        sites_list = db.query(Site.site_id, Site.site_code, Site.site_name, Site.created_by_id).filter(Site.status == active.miscellaneous_id).filter(Site.created_by_id.in_(user_ids)).order_by(desc(Site.created)).all()
        try:
            if sites_list:
                sites  = []
                for sitestatus in sites_list:
                    # status = ""
                    obj ={}
                    site_rec_pop = db.query(Rec_Population_grp).filter(Rec_Population_grp.site_id == sitestatus.site_id).all()
                    site_rec_icd_table = db.query(Siteicd).filter(Siteicd.site_id == sitestatus.site_id).all()
                    site_rec_hospital_table = db.query(SiteRecHospitalInfra).filter(SiteRecHospitalInfra.site_id == sitestatus.site_id).all()
                    site_rec_cr_infra_table = db.query(Cr_infra).filter(Cr_infra.site_id == sitestatus.site_id).all()
                    site_rec_it_table = db.query(It).filter(It.site_id == sitestatus.site_id).all()
                    site_rec_hr_table = db.query(Siterec_hr).filter(Siterec_hr.site_id == sitestatus.site_id).all()
                    # site_rec_cr_table = db.query(Cr).filter(Cr.site_id == sitestatus.site_id).all()
                    site_rec_reg_table = db.query(RegulatoryInfo).filter(RegulatoryInfo.site_id == sitestatus.site_id).all()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    results = db.query(Upload_Documents).filter(Upload_Documents.site_id == sitestatus.site_id,Upload_Documents.screen_type_name == "Site Recognition",Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()
                    no_results = db.query(Upload_Documents).filter(Upload_Documents.site_id == sitestatus.site_id,Upload_Documents.screen_type_name == "Site Recognition",Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
    
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
                                            # "cr_id": item["cr_id"],
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

                    document_status = None
                    if final_result:
                        org_id = db.query(User).filter(User.id == sitestatus.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
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

                        # document_status = None  
                        if(pending_verification_obj and approved_document_obj and rejected_document_obj):
                            if all(status is None or status == pending_verification_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending"    
                            obj['document_status'] = document_status
                        else:
                            obj['document_status'] = "Not Started"
   
                    elif no_results :
                        obj['document_status'] = "Pending"    
                        
                    else:
                        obj['document_status'] = "Not Started"

                    if site_rec_pop and site_rec_icd_table and site_rec_hospital_table and site_rec_cr_infra_table and site_rec_it_table and site_rec_hr_table and site_rec_reg_table and obj['document_status'] == 'Completed':
                        status = "Completed"
                    elif site_rec_pop or site_rec_icd_table or site_rec_hospital_table or site_rec_cr_infra_table or site_rec_it_table or site_rec_hr_table  or site_rec_reg_table or obj['document_status'] == 'Pending' or obj['document_status'] == 'Rejected': 
                        status = "In Progress"
                    else :
                        status = "Not Started"
                    
                    obj['site_id'] = sitestatus.site_id
                    obj['site_code'] = sitestatus.site_code
                    obj['site_name'] = sitestatus.site_name
                    obj['value'] = status

                    sites.append(obj)    

                return {"sites" : sites}
                # return user

        finally:
            db.close()

    def search_sites_rec(self,site_id,site_rec_status):
        db = next(get_db())
        try:
            if site_id and site_rec_status :
                site_rec_list = db.query(Site.site_id, Site.site_code, Site.site_name, Miscellaneous.value).join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.site_rec_status).filter(and_(Site.site_id == site_id, Site.site_rec_status == site_rec_status)).all()
                return {"site_rec_list" : site_rec_list}
            if site_rec_status :
                site_rec_list = db.query(Site.site_id, Site.site_code, Site.site_name, Miscellaneous.value).join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.site_rec_status).filter(Site.site_rec_status == site_rec_status).all()
                return {"site_rec_list" : site_rec_list}
            if site_id :
                site_rec_list = db.query(Site.site_id, Site.site_code, Site.site_name, Miscellaneous.value).join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.site_rec_status).filter(Site.site_id == site_id).all()
                return {"site_rec_list" : site_rec_list}
            else :
                return {"code": "fields are empty"}
        finally:
            db.close()

    def miscellaneous_sites_rec(self):
        db = next(get_db())
        try:
            site_rec_status= db.query(Miscellaneous.miscellaneous_id,Miscellaneous.value).filter(Miscellaneous.type == "status").all()
            return {"site_rec_list" : site_rec_status}
        finally:
            db.close()

    def miscellaneous_sites_by_type(self,mis_type):
        db = next(get_db())
        try:
            site_rec_status= db.query(Miscellaneous.miscellaneous_id,Miscellaneous.value).filter(Miscellaneous.type == mis_type).all()
            return {"site_rec_list" : site_rec_status}
        finally:
            db.close()

    def get_sites_assess_status(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()       
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]
        active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
        # sites_list = db.query(Site).filter(Site.status == active.miscellaneous_id).order_by(desc(Site.created)).all()
        sites_list = db.query(Site).filter(Site.status == active.miscellaneous_id).filter(Site.created_by_id.in_(user_ids)).order_by(desc(Site.created)).all()
        
        try:
            sites = []
            
            for site in sites_list:
                obj ={}
                registration = db.query(Site_Assess_Registration).filter(Site_Assess_Registration.site_id == site.site_id).first()
                infra = db.query(SiteAsmtInfrastructure).filter(SiteAsmtInfrastructure.site_id == site.site_id).first()
                legal = db.query(Legal).filter(Legal.site_id == site.site_id).first()
                review = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_id == site.site_id).first()
                org_personal = db.query(Orgpersonal).filter(Orgpersonal.site_id == site.site_id).first()
                quality = db.query(QualitySystems).filter(QualitySystems.site_id == site.site_id).first()
                
                upload_documents = db.query(Upload_Documents).filter(Upload_Documents.site_id == site.site_id,Upload_Documents.screen_type_name == "Site Assessment").all()
                no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                results = db.query(Upload_Documents).filter(Upload_Documents.site_id == site.site_id,Upload_Documents.screen_type_name == "Site Assessment",Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()
                no_results = db.query(Upload_Documents).filter(Upload_Documents.site_id == site.site_id,Upload_Documents.screen_type_name == "Site Assessment",Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                final_result = []

                if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
    
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
                                            # "cr_id": item["cr_id"],
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


                document_status = None
                if final_result:
                    
                    org_id = db.query(User).filter(User.id == site.created_by_id).first()
                    users = db.query(User).filter(User.org_id == org_id.org_id).all()
                    pending_document_list = []
                    for user in users:
                        pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                        if(pending_status):
                            pending_document_list.extend(pending_status)
                    pending_document_obj = None        
                    for document in pending_document_list:
                        if document.document_status_description.lower() == "pending document":
                            pending_document_obj = document
                            break 
                            
                    pending_verification_list = []
                    for user in users:
                        verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                        if(verification_status):
                            pending_verification_list.extend(verification_status)
                    pending_verification_obj = None        
                    for document in pending_verification_list:
                        if document.document_status_description.lower() == "pending verification":
                            pending_verification_obj = document
                            break 

                    approved_document_list = []
                    for user in users:
                        approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                        if(approved_status):
                            approved_document_list.extend(approved_status)
                    approved_document_obj = None        
                    for document in approved_document_list:
                        if document.document_status_description.lower() == "approved":
                            approved_document_obj = document
                            break      

                    rejected_document_list = []
                    for user in users:
                        rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                        if(rejected_status):
                            rejected_document_list.extend(rejected_status)
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

                        # document_status = None 
                    if(pending_verification_obj and approved_document_obj and rejected_document_obj):     
                        if all(status is None or status == pending_verification_obj.documentstatus_id for status in documents_list):
                            document_status = "Pending"
                        elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                            document_status = "Completed"
                        elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                            document_status = "Rejected"
                        elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                            document_status = "Pending"
                        obj['document_status'] = document_status 
                    else:
                        obj['document_status'] = "Not Started"    
                elif no_results :
                    obj['document_status'] = "Pending"    
                else:     
                    obj['document_status'] = "Not Started"    
                # status = ""
                
                if(registration and infra and legal and review and org_personal and quality and obj['document_status'] == 'Completed'):
                    status = "Completed"
                elif(registration or infra or legal or review or org_personal or quality or obj['document_status'] == 'Pending' or obj['document_status'] == 'Rejected'):
                    status = "In Progress"  
                else:
                    status = "Not Started" 
                # print(document_status)     
                # print(status)    

                obj['site_id'] = site.site_id
                obj['site_code'] = site.site_code
                obj['site_name'] = site.site_name
                obj['status'] = status     
                     
                
                sites.append(obj)    
            return sites

        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

     
    def get_cr_status(self):
        db = next(get_db())
        active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
        sites = db.query(Site).filter(Site.status == active.miscellaneous_id).order_by(desc(Site.created)).all()
        try:
            sites_dict = {} 
            for site in sites:
                site_info = {
                    "site_id": site.site_id,
                    "site_code": site.site_code,
                    "site_name": site.site_name
                }

                sites_list = db.query(Site.site_id, Site.site_code, Cr.cr_code, Cr.site_rec_cr_id) \
                    .outerjoin(Cr, Cr.site_id == Site.site_id).filter(Site.site_id == site.site_id).all()

                status = []
                for cr in sites_list:
                    general = db.query(General).filter(General.cr_code == cr.site_rec_cr_id).filter(General.site_id == cr.site_id).first()
                    if(general):
                        status.append(1)
                        facilities = db.query(GeneralAffiliations).filter(GeneralAffiliations.cr_general_id == general.cr_general_id).first()
                        education = db.query(GeneralEducation).filter(GeneralEducation.cr_general_id == general.cr_general_id).first()
                        if(facilities):
                            status.append(1)
                        else:
                            status.append(0)

                        if(education):
                            status.append(1)
                        else:
                            status.append(0)    
                    else:
                        status.append(0)

                    check_list = db.query(Cr_Research_Exp_Check_List).filter(Cr_Research_Exp_Check_List.cr_code == cr.site_rec_cr_id).filter(Cr_Research_Exp_Check_List.site_id == cr.site_id).first()
                    if(check_list):
                        status.append(1) 
                        professional_exp = db.query(Cr_Professional_Experience).filter(Cr_Professional_Experience.cr_res_exp_check_list_id == check_list.cr_res_exp_check_list_id).first()
                        if(professional_exp):
                            status.append(1)
                        else:
                            status.append(0)

                        cr_license = db.query(Cr_License_Ense).filter(Cr_License_Ense.cr_res_exp_check_list_id == check_list.cr_res_exp_check_list_id).first()
                        if(cr_license):
                            status.append(1)
                        else:
                            status.append(0)

                        gcp_trai = db.query(Cr_Gcp_Trai).filter(Cr_Gcp_Trai.cr_res_exp_check_list_id == check_list.cr_res_exp_check_list_id).first()
                        if(gcp_trai):
                            status.append(1)
                        else:
                            status.append(0)

                        cr_specialities = db.query(Cr_Specialities).filter(Cr_Specialities.cr_res_exp_check_list_id == check_list.cr_res_exp_check_list_id).first()
                        if(cr_specialities):
                            status.append(1)
                        else:
                            status.append(0)

                        total_research = db.query(Cr_Total_Clinical_Research_Exp).filter(Cr_Total_Clinical_Research_Exp.cr_res_exp_check_list_id == check_list.cr_res_exp_check_list_id).first()
                        if(total_research):
                            status.append(1)
                        else:
                            status.append(0)               
                    else:
                        status.append(0)
                    

                if any(status):  
                    if all(status):  
                        final_status = "Completed"
                    else:
                        final_status = "In Progress"
                else:
                    final_status = "Not Started"   

                site_info["status"] = final_status  
                sites_dict[site.site_id] = site_info  

            sites_status_list = list(sites_dict.values())

            return sites_status_list
        finally:
                db.close()    


