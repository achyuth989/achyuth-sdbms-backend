from app.model.user import User
from app.model.cr_status import Cr_Status
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc,asc

class Cr_Status_Service:
    def add_cr_status(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_status_list = []
        for user in users:
            cr_status = db.query(Cr_Status).filter(Cr_Status.created_by_id == user.id).all()
            if(cr_status):
                existing_status_list.extend(cr_status)
        check_existing_status = False
        if any(existing_status.cr_id.lower() == data.cr_id.lower() for existing_status in existing_status_list):
            check_existing_status = True
        try:
            # cr_id = db.query(Cr_Status).filter(func.lower(Cr_Status.cr_id) == data.cr_id.lower()).first()
            # cr_status = db.query(Cr_Status).filter(func.lower(Cr_Status.cr_status) == data.cr_status.lower()).first()
            if(check_existing_status):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="CR id already exists")
            # elif(cr_status):
            #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="CR Status already exists")    
            else:    
                new_cr_status = Cr_Status(
                    cr_id = data.cr_id,
                    cr_status = data.cr_status,
                    description = data.description,
                    created_by_id = data.created_by_id
                )
                db.add(new_cr_status)
                db.commit()
                db.refresh(new_cr_status)
                return{"response":"CR status added Successfully"}
       
        finally:        
            db.close()


    def get_cr_status(self,user_id):
        db = next(get_db())
        try:
            # get data by org, taking user_id as input paramter

            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            
            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    added_cr_status =[]
                    for user in list_of_users_related_to_org:
                        cr_status = db.query(Cr_Status).filter(Cr_Status.created_by_id==user.id).order_by((Cr_Status.created)).all()
                        # doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.created_by_id==user.id).order_by(desc(DocumentCategory.created)).all()
                        added_cr_status.extend(cr_status)
                    return {"response":added_cr_status}
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
    def cr_status(self,id):
        db = next(get_db())
        try:
            cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == id).all()
            return{"response":cr_status}  
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:        
            db.close()
    def update_cr_status(self,id,data):
        db = next(get_db())
        
        
        get_data_from_id = db.query(Cr_Status).filter(Cr_Status.cr_status_id == id).first()
        get_org_for_this_record = db.query(User).filter(User.id == get_data_from_id.created_by_id).first()
        
        get_users_for_this_org = db.query(User).filter(User.org_id == get_org_for_this_record.org_id).all()
        
        status_description_list = []
        for user in get_users_for_this_org:
            status_description = db.query(Cr_Status).filter(Cr_Status.created_by_id == user.id).all()
            if status_description:
                status_description_list.extend(status_description)

        check_existing_status = False
        if any(existing_status.cr_status.lower() == data.cr_status.lower().strip() for existing_status in status_description_list):
            check_existing_status = True          

        cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == id).first()
        status_name = db.query(Cr_Status).filter(func.lower(Cr_Status.cr_status) == data.cr_status.lower()).filter(Cr_Status.cr_status_id != id).first()
        try:
            if(check_existing_status):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="CR Status already exists for this organization")    
            else:    
                if(cr_status):
                    cr_status.cr_status = data.cr_status,
                    cr_status.description = data.description,
                    cr_status.updated_by_id = data.updated_by_id
                    db.commit()
                    return{"response":"CR status updated Successfully"}
                else:
                    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "CR status not found")
        
        finally:        
            db.close()