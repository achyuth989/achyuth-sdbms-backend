from app.model.user import User
from app.model.documents import Documents
from app.model.document_category import DocumentCategory
from fastapi import HTTPException, status
from  app.model.site import Site
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func, desc

class Documents_Service:
    def add_documents(self,data):
        db = next(get_db())
        document_check = False
        try:
            for document in data.AdditionalDoc:
                existing_document = db.query(Documents).filter(Documents.site_id == data.site_id).filter(func.lower(Documents.document_description) == document.document_description.lower()).first()
                if(existing_document):
                    document_check = True
            if(document_check == True):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Document already exist for this Site.")
            else:
                for documents in data.AdditionalDoc:
                    new_document = Documents(
                        site_id = data.site_id,
                        short_name = documents.short_name,
                        document_description = documents.document_description,
                        caterogy = data.caterogy,
                        remarks = documents.remarks,
                        created_by_id = data.created_by_id
                    )
                    db.add(new_document)
                    db.commit()
                    db.refresh(new_document)
                return{"response":"Documents added Successfully"}   

        # existing_document = db.query(Documents).filter(Documents.site_id == data.site_id).filter(func.lower(Documents.document_description) == data.document_description.lower()).first()
        # if(existing_document):
        #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Document already exist for this Site.")
        # try:
        #     new_document = Documents(
        #         site_id = data.site_id,
        #         # document_code = data.document_code,
        #         short_name = data.short_name,
        #         document_description = data.document_description,
        #         caterogy = data.caterogy,
        #         remarks = data.remarks,
        #         created_by_id = data.created_by_id
        #     )
        #     db.add(new_document)
        #     db.commit()
        #     db.refresh(new_document)
        #     return{"response":"Document added Successfully"}
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
       

    def get_documents(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()       
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]
        try:
            documents = db.query(Documents.document_id,Documents.created_by_id,Documents.site_id,Documents.short_name,Documents.document_description,Documents.remarks,DocumentCategory.document_category_id,DocumentCategory.document_category,DocumentCategory.description, Site.site_name, Site.site_code).join(Site, Site.site_id == Documents.site_id).join(DocumentCategory, DocumentCategory.document_category_id == Documents.caterogy).filter(Documents.created_by_id.in_(user_ids)).order_by(desc(Documents.created)).all()
            return {"response":documents}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    # def documents(self,id):
    #     db= next(get_db())
    #     try:
    #         documents = db.query(Documents.document_id,Documents.site_id,Documents.short_name,Documents.document_description,Documents.remarks,DocumentCategory.document_category_id,DocumentCategory.document_category,DocumentCategory.description,Site.site_name,Site.site_code).join(Site, Site.site_id == Documents.site_id).join(DocumentCategory, DocumentCategory.document_category_id == Documents.caterogy).filter(Documents.site_id == id).order_by(desc(Documents.created)).all()
    #         return {"response":documents}    
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    #     finally:
    #         db.close()
    
    def documents(self, id):
        db = next(get_db())
        try:
            documents = db.query(
                Documents.document_id, Documents.site_id, Documents.short_name,
                Documents.document_description, Documents.remarks,
                DocumentCategory.document_category_id, DocumentCategory.document_category,
                DocumentCategory.description, Site.site_name, Site.site_code
            ).join(Site, Site.site_id == Documents.site_id).join(
                DocumentCategory, DocumentCategory.document_category_id == Documents.caterogy
            ).filter(Documents.site_id == id).order_by(desc(Documents.created)).all()

            document_dict = {}
            for document in documents:
                description = document.description
                if description not in document_dict:
                    document_dict[description] = []
                document_dict[description].append({
                    "document_id": document.document_id,
                    "site_id": document.site_id,
                    "short_name": document.short_name,
                    "document_description": document.document_description,
                    "remarks": document.remarks,
                    "document_category_id": document.document_category_id,
                    "document_category": document.document_category,
                    "site_name": document.site_name,
                    "site_code": document.site_code
                })

            return {"response":documents}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_documents(self,id,data):
        db= next(get_db())
        
        get_data_from_id = db.query(Documents).filter(Documents.document_id == id).first()
        get_org_for_this_record = db.query(User).filter(User.id == get_data_from_id.created_by_id).first()
        
        get_users_for_this_org = db.query(User).filter(User.org_id == get_org_for_this_record.org_id).all()
        
        status_description_list = []
        for user in get_users_for_this_org:
            status_description = db.query(Documents).filter(Documents.created_by_id == user.id).all()
            if status_description:
                status_description_list.extend(status_description)

        check_existing_status = False
        if any(existing_status.document_description.lower() == data.document_description.lower().strip() for existing_status in status_description_list):
            check_existing_status = True  
        
        
        documents = db.query(Documents).filter(Documents.document_id == id).first()
        # existing_document = db.query(Documents).filter(Documents.site_id == data.site_id).filter(func.lower(Documents.document_description) == data.document_description.lower()).filter(Documents.document_id != id).first()
        try:
            if(check_existing_status):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Document already exists for this org")
            if(documents):
                documents.short_name = data.short_name,
                documents.document_description = data.document_description,
                # documents.caterogy = data.caterogy,
                documents.remarks = data.remarks,
                documents.updated_by_id = data.updated_by_id
                db.commit()
                return {"response":"Documents updated Successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Documents not found")
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()           