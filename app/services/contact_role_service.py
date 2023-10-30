from app.model.contact_role import ContactRole
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func,desc,asc
from app.model.user import User


class Contact_Role:
    def add_contact_roles(self,data):
        db = next(get_db())
        try:
            print(data.contact_id)
            contact_id = db.query(ContactRole).filter(func.lower(ContactRole.contact_id) == data.contact_id.lower()).first()
            contact_role = db.query(ContactRole).filter(func.lower(ContactRole.contact_role) == data.contact_role.lower()).first()
            if(contact_id):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Contact id already exists")
            elif(contact_role):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Contact Role already exists")    
            else:    
                new_contact_role = ContactRole(
                    contact_id = data.contact_id,
                    contact_role = data.contact_role,
                    description = data.description,
                    created_by_id = data.created_by_id
                )
                db.add(new_contact_role)
                db.commit()
                db.refresh(new_contact_role)
                return{"response":"Contact Role added Successfully"}
        finally:
            db.close()        

    def get_contact_roles(self,user_id):
        db = next(get_db())
        try:
            # get data by org, taking user_id as input paramter

            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            
            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    added_contact_role =[]
                    for user in list_of_users_related_to_org:
                        contact_role = db.query(ContactRole).filter(ContactRole.created_by_id==user.id).order_by((ContactRole.created)).all()
                        # doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.created_by_id==user.id).order_by(desc(DocumentCategory.created)).all()
                        added_contact_role.extend(contact_role)
                    return {"response":added_contact_role}
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}
            
            
            # cr_status = db.query(Cr_Status).order_by((Cr_Status.created)).all()
            # return{"response":cr_status}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:        
            db.close()
   

    def  update_contact_roles(self,id,data):
        db = next(get_db())
        contact_role = db.query(ContactRole).filter(ContactRole.contact_role_id == id).first()
        role_name = db.query(ContactRole).filter(func.lower(ContactRole.contact_role) == data.contact_role.lower()).filter(ContactRole.contact_role_id != id).first()
        try:
            if(role_name):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Contact Role already exists")    
            else:    
                if(contact_role):
                    contact_role.contact_role = data.contact_role,
                    contact_role.description = data.description,
                    contact_role.updated_by_id = data.updated_by_id
                    db.commit()
                    return{"response":"Contact Role updated Successfully"}
                else:
                    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Contact Role not found")
        
        finally:        
            db.close()