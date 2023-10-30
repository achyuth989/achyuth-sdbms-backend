from app.model.user import User
from app.model.audit_log import AuditLog
from app.model.upload_documents import Upload_Documents
from app.model.general import General
from app.model.cr_professional_experience import Cr_Research_Exp_Check_List
import datetime
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func, or_, desc
from app.model.cr_status import Cr_Status



class Audit_Log_Service:
    def get_recognition_audit_log(self,id):
        db= next(get_db())
        response = {}
        try:
            latest_updated = db.query(AuditLog).filter(or_(AuditLog.table_name == "site_rec_pop_group", AuditLog.table_name == "site_rec_icd", AuditLog.table_name == "site_rec_hospital_infra", AuditLog.table_name == "site_rec_cr_infra", AuditLog.table_name == "site_rec_it_systems_infra", AuditLog.table_name == "site_rec_hr", AuditLog.table_name == "site_rec_cr", AuditLog.table_name == "site_rec_regulatory_information")).filter(AuditLog.site_id == id).filter(AuditLog.action == "UPDATE").order_by(desc(AuditLog.action_date)).first()
            latest_created = db.query(AuditLog).filter(or_(AuditLog.table_name == "site_rec_pop_group", AuditLog.table_name == "site_rec_icd", AuditLog.table_name == "site_rec_hospital_infra", AuditLog.table_name == "site_rec_cr_infra", AuditLog.table_name == "site_rec_it_systems_infra", AuditLog.table_name == "site_rec_hr", AuditLog.table_name == "site_rec_cr", AuditLog.table_name == "site_rec_regulatory_information")).filter(AuditLog.site_id == id).filter(AuditLog.action == "INSERT").order_by(desc(AuditLog.action_date)).first()
            created_documents = db.query(Upload_Documents).filter(Upload_Documents.screen_type_name == "Site Recognition").filter(Upload_Documents.site_id == id).order_by(desc(Upload_Documents.created)).first()
            updated_documents = db.query(Upload_Documents).filter(Upload_Documents.screen_type_name == "Site Recognition").filter(Upload_Documents.site_id == id).filter(Upload_Documents.updated != None).order_by(desc(Upload_Documents.updated)).first()

            if(created_documents):
                timestamp1 = latest_created.action_date
                timestamp2 = created_documents.created
                audit_latest_created = latest_created.action_date
                documents_latest_created = created_documents.created
                if(audit_latest_created > documents_latest_created):
                    latest_created_user = latest_created.performed_by_id
                else:
                    latest_created_user = created_documents.created_by_id
                latest_created_timestamp = max(timestamp1, timestamp2)
                created_user = db.query(User).filter(User.id == latest_created_user).first()
                response["created_by"] = created_user.name
                response["created_on"] = latest_created_timestamp

            elif(latest_created):
                created_user = db.query(User).filter(User.id == latest_created.performed_by_id).first()
                response["created_by"] = created_user.name
                response["created_on"] = latest_created.action_date
            else:
                response["created_by"] = ""
                response["created_on"] = ""
                
            if(updated_documents):
                if(latest_updated):
                    timestamp3 = latest_updated.action_date
                else:
                    timestamp3 = datetime.datetime.today() - datetime.timedelta(days=365)

                timestamp4 = updated_documents.updated
                if(latest_updated):
                    audit_latest_updated = latest_updated.action_date
                else:
                    audit_latest_updated = datetime.datetime.today() - datetime.timedelta(days=365)
    
                documents_latest_updated = updated_documents.updated
                if(audit_latest_updated > documents_latest_updated):
                    latest_updated_user = latest_updated.performed_by_id
                else:
                    latest_updated_user = updated_documents.updated_by_id
                latest_updated_timestamp = max(timestamp3, timestamp4)
                updated_user = db.query(User).filter(User.id == latest_updated_user).first()
                response["updated_by"] = updated_user.name
                response["updated_on"] = latest_updated_timestamp

            elif(latest_updated):  
                updated_user = db.query(User).filter(User.id == latest_updated.performed_by_id).first()
                response["updated_by"] = updated_user.name
                response["updated_on"] = latest_updated.action_date
            else:
                response["updated_by"] = ""
                response["updated_on"] = ""  
                
            return response
        finally:
            db.close()    

    def get_assessment_audit_log(self,id):
        db= next(get_db())
        response = {}
        try:
            latest_updated = db.query(AuditLog).filter(or_(AuditLog.table_name == "site_asmt_reg_ser", AuditLog.table_name == "site_asmt_org_pers", AuditLog.table_name == "site_asmt_quality_sys", AuditLog.table_name == "site_asmt_infra_equal", AuditLog.table_name == "site_asmt_doc", AuditLog.table_name == "site_asmt_reviewer")).filter(AuditLog.site_id == id).filter(AuditLog.action == "UPDATE").order_by(desc(AuditLog.action_date)).first()
            latest_created = db.query(AuditLog).filter(or_(AuditLog.table_name == "site_asmt_reg_ser", AuditLog.table_name == "site_asmt_org_pers", AuditLog.table_name == "site_asmt_quality_sys", AuditLog.table_name == "site_asmt_infra_equal", AuditLog.table_name == "site_asmt_doc", AuditLog.table_name == "site_asmt_reviewer")).filter(AuditLog.site_id == id).filter(AuditLog.action == "INSERT").order_by(desc(AuditLog.action_date)).first()
            created_documents = db.query(Upload_Documents).filter(Upload_Documents.screen_type_name == "Site Assessment").filter(Upload_Documents.site_id == id).order_by(desc(Upload_Documents.created)).first()
            updated_documents = db.query(Upload_Documents).filter(Upload_Documents.screen_type_name == "Site Assessment").filter(Upload_Documents.site_id == id).filter(Upload_Documents.updated != None).order_by(desc(Upload_Documents.updated)).first()

            if(created_documents):
                timestamp1 = latest_created.action_date
                timestamp2 = created_documents.created
                audit_latest_created = latest_created.action_date
                documents_latest_created = created_documents.created
                if(audit_latest_created > documents_latest_created):
                    latest_created_user = latest_created.performed_by_id
                else:
                    latest_created_user = created_documents.created_by_id
                latest_created_timestamp = max(timestamp1, timestamp2)
                created_user = db.query(User).filter(User.id == latest_created_user).first()
                response["created_by"] = created_user.name
                response["created_on"] = latest_created_timestamp

            elif(latest_created):
                created_user = db.query(User).filter(User.id == latest_created.performed_by_id).first()
                response["created_by"] = created_user.name
                response["created_on"] = latest_created.action_date
            else:
                response["created_by"] = ""
                response["created_on"] = ""
                
            if(updated_documents):
                if(latest_updated):
                    timestamp3 = latest_updated.action_date
                else:
                    timestamp3 = datetime.datetime.today() - datetime.timedelta(days=365)    
                timestamp4 = updated_documents.updated
                if(latest_updated):
                    audit_latest_updated = latest_updated.action_date
                else:
                    audit_latest_updated = datetime.datetime.today() - datetime.timedelta(days=365)    
                documents_latest_updated = updated_documents.updated
                if(audit_latest_updated > documents_latest_updated):
                    latest_updated_user = latest_updated.performed_by_id
                else:
                    latest_updated_user = updated_documents.updated_by_id
                latest_updated_timestamp = max(timestamp3, timestamp4)
                updated_user = db.query(User).filter(User.id == latest_updated_user).first()
                response["updated_by"] = updated_user.name
                response["updated_on"] = latest_updated_timestamp

            elif(latest_updated):  
                updated_user = db.query(User).filter(User.id == latest_updated.performed_by_id).first()
                response["updated_by"] = updated_user.name
                response["updated_on"] = latest_updated.action_date
            else:
                response["updated_by"] = ""
                response["updated_on"] = ""  
                
            return response  
        finally:
            db.close()      

            
    def get_cr_audit_log(self,id):
        db= next(get_db())
        response = {}
        try:
            general_created = db.query(General).filter(General.cr_general_id == id).order_by(desc(General.created)).first()
            general_updated = db.query(General).filter(General.cr_general_id == id).filter(General.updated != None).order_by(desc(General.updated)).first()

            check_list_created = db.query(Cr_Research_Exp_Check_List).filter(Cr_Research_Exp_Check_List.cr_general_id == id).order_by(desc(Cr_Research_Exp_Check_List.created)).first()
            check_list_updated = db.query(Cr_Research_Exp_Check_List).filter(Cr_Research_Exp_Check_List.cr_general_id == id).filter(Cr_Research_Exp_Check_List.updated != None).order_by(desc(Cr_Research_Exp_Check_List.updated)).first()
            

            created_documents = db.query(Upload_Documents).filter(Upload_Documents.screen_type_name == "Clinical Researcher").filter(Upload_Documents.cr_code == id).order_by(desc(Upload_Documents.created)).first()
            updated_documents = db.query(Upload_Documents).filter(Upload_Documents.screen_type_name == "Clinical Researcher").filter(Upload_Documents.cr_code == id).filter(Upload_Documents.updated != None).order_by(desc(Upload_Documents.updated)).first()

            if(created_documents):
                general_timestamp = general_created.created
                document_timestamp = created_documents.created
                
                check_list_timestamp = datetime.datetime.today() - datetime.timedelta(days=365)
                if(check_list_created):
                    check_list_timestamp = check_list_created.created
                valid_objects = [x for x in [general_created, check_list_created, created_documents] if x is not None and hasattr(x, 'created')]

                if valid_objects:
                    latest_object = max(valid_objects, key=lambda x: x.created)
                    created_user = db.query(User).filter(User.id == latest_object.created_by_id).first()
                    response["created_by"] = created_user.name
                    response["created_on"] = latest_object.created
                else:
                    response["created_by"] = ""
                    response["created_on"] = ""
            elif(general_created):
                general_timestamp = general_created.created
                document_timestamp = datetime.datetime.today() - datetime.timedelta(days=365)
                check_list_timestamp = datetime.datetime.today() - datetime.timedelta(days=365)
                if(check_list_created):
                    check_list_timestamp = check_list_created.created
                if(created_documents):
                    document_timestamp = created_documents.created
                valid_objects = [x for x in [general_created, check_list_created, created_documents] if x is not None and hasattr(x, 'created')]

                if valid_objects:
                    latest_object = max(valid_objects, key=lambda x: x.created)
                    created_user = db.query(User).filter(User.id == latest_object.created_by_id).first()
                    response["created_by"] = created_user.name
                    response["created_on"] = latest_object.created
                else:
                    response["created_by"] = ""
                    response["created_on"] = ""   
            else:
                response["created_by"] = ""
                response["created_on"] = ""         
                
            if(updated_documents):
                if(general_updated):
                    general_timestamp = general_updated.updated
                else:
                    general_timestamp = datetime.datetime.today() - datetime.timedelta(days=365)   
                document_timestamp = updated_documents.updated
                
                check_list_timestamp = datetime.datetime.today() - datetime.timedelta(days=365)
               
                if(check_list_updated):
                    check_list_timestamp = check_list_updated.updated
                latest_updated_timestamp = max(general_timestamp, document_timestamp, check_list_timestamp)
                valid_objects = [x for x in [general_updated, check_list_updated, updated_documents] if x is not None and hasattr(x, 'updated')]

                if valid_objects:
                    latest_object = max(valid_objects, key=lambda x: x.updated)
                    updated_user = db.query(User).filter(User.id == latest_object.updated_by_id).first()
                    response["updated_by"] = updated_user.name
                    response["updated_on"] = latest_object.updated
                else:
                    response["updated_by"] = ""
                    response["updated_on"] = ""
            elif(general_updated):
                general_timestamp = general_updated.updated
                document_timestamp = datetime.datetime.today() - datetime.timedelta(days=365)
                check_list_timestamp = datetime.datetime.today() - datetime.timedelta(days=365)
                if(check_list_updated):
                    check_list_timestamp = check_list_updated.updated
                if(updated_documents):
                    document_timestamp = updated_documents.updated
                latest_updated_timestamp = max(general_timestamp, document_timestamp, check_list_timestamp)
                valid_objects = [x for x in [general_updated, check_list_updated, updated_documents] if x is not None and hasattr(x, 'updated')]

                if valid_objects:
                    latest_object = max(valid_objects, key=lambda x: x.updated)
                    updated_user = db.query(User).filter(User.id == latest_object.updated_by_id).first()
                    response["updated_by"] = updated_user.name
                    response["updated_on"] = latest_object.updated
                else:
                    response["updated_by"] = ""
                    response["updated_on"] = ""  
            else:
                response["updated_by"] = ""
                response["updated_on"] = ""          
            if(general_created):
                cr_status =  db.query(Cr_Status).filter(Cr_Status.cr_status_id == general_created.cr_status).first()
                response["cr_status"] = cr_status.cr_status
                response["reason_for_blocking"] = general_created.reason_for_blocking
            else:
                response["cr_status"] = ""
                response["reason_for_blocking"] = ""    
           

            return response
        finally:
            db.close()   

    def reason_for_blocking(self,data):
        db = next(get_db())
        try:
            cr = db.query(General).filter(General.cr_general_id == data.cr_id).first()
            if(cr):
                cr.reason_for_blocking = data.reason_for_blocking
                cr.updated_by_id = data.updated_by_id
                db.commit()
                return "reason added successfully"
            else:
                raise HTTPException(status_code=404, detail="CR id doesn't exist")           
        finally:
            db.close()