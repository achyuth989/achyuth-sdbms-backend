from app.model.document_category import DocumentCategory
from fastapi import HTTPException, status
from app.db.database import get_db
from sqlalchemy import func,desc
from app.model.user import User

class Document_Category_Service():
    def add_document_category(self, document_details):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == document_details.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_category_list = []
        for user in users:
            categories = db.query(DocumentCategory).filter(DocumentCategory.created_by_id == user.id).all()
            if(categories):
                existing_category_list.extend(categories)
        check_existing_category = False
        if any(existing_category.document_category.lower() == document_details.document_category.lower() for existing_category in existing_category_list):
            check_existing_category = True  
        document_id = db.query(DocumentCategory).filter(func.lower(DocumentCategory.document_category) == document_details.document_category.lower()).first()
        if check_existing_category:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Document category already exist.")
        else :
            try:
                new_document_category = DocumentCategory(
                    document_category = document_details.document_category,
                    description = document_details.description,
                    created_by_id = document_details.created_by_id
                )
                db.add(new_document_category)
                db.commit()
                db.refresh(new_document_category)
                return {"success": "Document category added successfully."}
            # except Exception as e:
            #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            finally:
                db.close()
    def document_category_list(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    added_documents_list =[]
                    for user in list_of_users_related_to_org:
                        doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.created_by_id==user.id).order_by(desc(DocumentCategory.created)).all()
                        added_documents_list.extend(doc_category_list)
                    return {"document_category_list": added_documents_list}
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_document(self,id,data):
        db = next(get_db())
        updatedocumentcatgry = db.query(DocumentCategory).filter(DocumentCategory.document_category_id == id).first()
        try:
            if(updatedocumentcatgry):
                updatedocumentcatgry.description=data.description,
                updatedocumentcatgry.updated_by_id=data.updated_by_id
                db.commit()
                return{"response":"Document category Updated Successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Document category not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
    def get_document_category(self,id):
        db = next(get_db())
        try:
            doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.document_category_id == id).first()
            return {"document_category_list": doc_category_list}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()