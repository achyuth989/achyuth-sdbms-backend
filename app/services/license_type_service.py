from app.db.database import get_db
from app.model.license_type import LicenseType
from fastapi import HTTPException, status
from sqlalchemy import func,desc
from app.model.user import User

class License_Type_Service():
    def add_license_type(self, license_details):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == license_details.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_license_list = []
        for user in users:
            license_type = db.query(LicenseType).filter(LicenseType.created_by_id == user.id).all()
            if(license_type):
                existing_license_list.extend(license_type)
        check_existing_license = False
        if any(existing_license.license_id.lower() == license_details.license_id.lower() for existing_license in existing_license_list):
            check_existing_license = True
        # license_ids =  db.query(LicenseType).filter(func.lower(LicenseType.license_id) == license_details.license_id.lower()).first()
        if check_existing_license:
            raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail="License id already exist.")
        else :
            try:
                new_license = LicenseType(
                    license_id	= license_details.license_id,
                    license_type = license_details.license_type,
                    description	= license_details.description,
                    created_by_id = license_details.created_by_id
                )
                db.add(new_license)
                db.commit()
                db.refresh(new_license)
                return {"success" : "License type added successfully."}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            finally :
                db.close()

    def license_type_list(self,user_id):
        db = next(get_db())
        try:

            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    license_type_list =[]
                    for user in list_of_users_related_to_org:
                        license_type = db.query(LicenseType).filter(LicenseType.created_by_id==user.id).order_by(desc(LicenseType.created)).all()
                        # doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.created_by_id==user.id).order_by(desc(DocumentCategory.created)).all()
                        license_type_list.extend(license_type)
                    return {"license_type_list":license_type_list} 
                else:
                    return {"response":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"response":f"user_id = {user_id} not found"}
            

            
            # license_type_lists = db.query(LicenseType).order_by(desc(LicenseType.created)).all()
            # return {"license_type_list": license_type_lists}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_license_type(self, id, data):
        db = next(get_db())
        updatelicensetype = db.query(LicenseType).filter(LicenseType.license_type_id == id).first()
        try:
            if(updatelicensetype):
                updatelicensetype.license_type=data.license_type,
                updatelicensetype.description  = data.description,
                updatelicensetype.updated_by_id  = data.updated_by_id,
                db.commit()
                return {"success": "License Type updated successfully."}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="License Type  id not found.")   
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_license_type(self,id):
        db = next(get_db())
        try:
            license_type_lists = db.query(LicenseType).filter(LicenseType.license_type_id == id).first()
            return {"license_type_list": license_type_lists}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()