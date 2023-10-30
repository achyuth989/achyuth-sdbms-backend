from app.model.document_status import Document_Status
from fastapi import HTTPException,status
from app.db.database import get_db 
from sqlalchemy import func,desc
from app.model.user import User

class  Document_Statuss:
    def Document_Status(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_status_list = []
        for user in users:
            document_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
            if(document_status):
                existing_status_list.extend(document_status)
        check_existing_status = False
        if any(existing_status.document_status_id.lower() == data.document_status_id.lower() for existing_status in existing_status_list):
            check_existing_status = True  
        # docmt_status = db.query(Document_Status).filter(func.lower(Document_Status.document_status_id) == data.document_status_id.lower()).first()
        # status_description = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == data.document_status_description.lower()).first()
        try:
            if check_existing_status:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Document Status ID already exist.")
            # elif(status_description):
            #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Document Status already exist.")    
            else:
                new_document = Document_Status(
                    document_status_id=data.document_status_id,
                    document_status_description=data.document_status_description,
                    created_by_id=data.created_by_id,
                )
                db.add(new_document)
                db.commit()
                return{"response":"Document status added"}
        
        finally:
            db.close()

    def get_document_status_all(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    added_documents_status =[]
                    for user in list_of_users_related_to_org:
                        status = db.query(Document_Status).filter(Document_Status.created_by_id==user.id).order_by(desc(Document_Status.created)).all()
                        # doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.created_by_id==user.id).order_by(desc(DocumentCategory.created)).all()
                        added_documents_status.extend(status)
                    return added_documents_status
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}
            
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_document_status_by_id(self,id):
        db = next(get_db())
        try:
            documentstatus = db.query(Document_Status).filter(Document_Status.documentstatus_id == id).all()
            return documentstatus
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_document_status(self,id,data):
        db = next(get_db())
        
        get_data_from_id = db.query(Document_Status).filter(Document_Status.documentstatus_id == id).first()
        get_org_for_this_record = db.query(User).filter(User.id == get_data_from_id.created_by_id).first()
        
        get_users_for_this_org = db.query(User).filter(User.org_id == get_org_for_this_record.org_id).all()
        
        status_description_list = []
        for user in get_users_for_this_org:
            status_description = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
            if status_description:
                status_description_list.extend(status_description)

        check_existing_status = False
        if any(existing_status.document_status_description.lower() == data.document_status_description.lower().strip() for existing_status in status_description_list):
            check_existing_status = True  
          
        updatedocumentstatus = db.query(Document_Status).filter(Document_Status.documentstatus_id == id).first()
        # status_description = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == data.document_status_description.lower()).filter(Document_Status.documentstatus_id != id).first()
        try:
            if(check_existing_status):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Document Status description already exists for this organization.")    
            else:    
                if(updatedocumentstatus):
                    updatedocumentstatus.document_status_description = data.document_status_description,
                    updatedocumentstatus.updated_by_id = data.updated_by_id,
                    db.commit()
                    return{"response":"document status updated sucessfully"}
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document status  not found.")
      
        finally:
            db.close()