from app.model.cr_roles import Cr_Roles
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func,desc,asc
from app.model.user import User

class Cr_Roless:
    def Cr_Roles(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_roles_list = []
        for user in users:
            cr_roles = db.query(Cr_Roles).filter(Cr_Roles.created_by_id == user.id).all()
            if(cr_roles):
                existing_roles_list.extend(cr_roles)
        check_existing_role = False
        if any(existing_role.cr_id.lower() == data.cr_id.lower() for existing_role in existing_roles_list):
            check_existing_role = True
        # cr_roless = db.query(Cr_Roles).filter(func.lower(Cr_Roles.cr_id) == data.cr_id.lower()).first()
        if check_existing_role:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="cr roles already exist.")
        else:
            try:
                new_crrole = Cr_Roles(
                    cr_id=data.cr_id,
                    cr_role=data.cr_role,
                    description=data.description,
                    created_by_id=data.created_by_id
                )
                db.add(new_crrole)
                db.commit()
                return{"success":"Sucessfully added CrRole"}
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create cr role.")
            finally:
                db.close()

    def get_cr_roles(self,user_id):
        db = next(get_db())
        try:
            # get data by org, taking user_id as input paramter

            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            
            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    cr_roles_list =[]
                    for user in list_of_users_related_to_org:
                        cr_roles = db.query(Cr_Roles).filter(Cr_Roles.created_by_id == user.id).order_by((Cr_Roles.created)).all()
                        cr_roles_list.extend(cr_roles)
                    return cr_roles_list
                else:
                    return {"response":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"response":f"user_id = {user_id} not found"}
            # cr_roles = db.query(Cr_Roles).order_by((Cr_Roles.created)).all()
            # return cr_roles
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
   
    def get_cr_roles_by_id(self,id):
        db = next(get_db())
        try:
            crroles = db.query(Cr_Roles).filter(Cr_Roles.cr_role_id == id).all()
            return crroles
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def  Update_cr_roles(self,id,data):
        db = next(get_db())
        updatecrroles = db.query(Cr_Roles).filter(Cr_Roles.cr_role_id == id).first()
        try:
            if(updatecrroles):
                updatecrroles.cr_role = data.cr_role,
                updatecrroles.description = data.description,
                updatecrroles.updated_by_id = data.updated_by_id
                db.commit()
                return{"response":"Cr Roles updated sucessfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cr Roles  not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()