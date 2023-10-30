from  app.model.role_master import Role_Master
from fastapi import HTTPException,status
from app.db.database import get_db 
from sqlalchemy import func,desc
from app.model.permissions import Permissions
from app.model.role_has_permissions import Role_Has_Permissions
from app.model.miscellaneous import Miscellaneous
from app.model.user import User

class Role_masters:
    def Role_Master_Services(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_role_list = []
        for user in users:
            roles = db.query(Role_Master).filter(Role_Master.created_by_id == user.id).all()
            if(roles):
                existing_role_list.extend(roles)
        check_existing_role = False
        if any(existing_role.role.lower() == data.role.lower() for existing_role in existing_role_list):
            check_existing_role = True
        try:
            roles_code = db.query(Role_Master).filter(func.lower(Role_Master.role) == data.role.lower()).first()
            miscellaneous_id = db.query(Miscellaneous).filter(Miscellaneous.type == "status", Miscellaneous.value == "1").first()
            if check_existing_role:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Role already exist.")
            else:
                new_roles = Role_Master(
                    role = data.role,
                    role_description = data.role_description,
                    status = miscellaneous_id.miscellaneous_id,
                    created_by_id = data.created_by_id
                )
                if data.permissions: 
                    db.add(new_roles)
                    db.commit()
                    db.refresh(new_roles)
                    for permission in data.permissions:
                        new_role_permissions = Role_Has_Permissions(
                            role_id = new_roles.role_master_id,
                            permissions_id = permission,
                            created_by_id = data.created_by_id
                        )
                        db.add(new_role_permissions)
                        db.commit()
                else :
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="permissions are empty at least one permission should select")
                return{"response":"Role Permissions added Successfully"}
        finally:
            db.close()
                
    def get_all_role_masters(self,org_id):
        db = next(get_db())
        try:
            user_data = db.query(User).filter(User.org_id == org_id).all()  
            roles_details = []
            if user_data:
                for user in user_data:
                    roles_masters = db.query(Role_Master).filter(Role_Master.created_by_id == user.id).all()  
                    for role in roles_masters:
                        role_dict = {
                            "role_master_id": role.role_master_id,
                            "role": role.role,
                            "role_description" : role.role_description,
                            "status": role.status
                        }
                        role_status = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == role.status).first()
                        permissions_list = db.query(Role_Has_Permissions).filter(Role_Has_Permissions.role_id == role.role_master_id).all()
                        role_dict["role_status"] = role_status.value
                        role_dict["permissions_list"] = permissions_list
                        roles_details.append(role_dict) 
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Org id has no users and roles.")
            roles_details = sorted(roles_details, key=lambda x: x['role_master_id'], reverse=True) 
            return{"response":roles_details}
        finally:        
            db.close()
    def get_all_active_role_masters(self,org_id):
        db = next(get_db())
        try:
            user_data = db.query(User).filter(User.org_id == org_id).all() 
            active_role = db.query(Miscellaneous).filter(Miscellaneous.type == "status" , Miscellaneous.value == "1").first() 
            roles_details = []
            if user_data:
                for user in user_data:
                    roles_masters = db.query(Role_Master).filter(Role_Master.created_by_id == user.id, Role_Master.status == active_role.miscellaneous_id).all()  
                    for role in roles_masters:
                        role_dict = {
                            "role_master_id": role.role_master_id,
                            "role": role.role,
                            "role_description" : role.role_description,
                            "status": role.status
                        }
                        role_status = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == role.status).first()
                        permissions_list = db.query(Role_Has_Permissions).filter(Role_Has_Permissions.role_id == role.role_master_id).all()
                        role_dict["role_status"] = role_status.value
                        role_dict["permissions_list"] = permissions_list
                        roles_details.append(role_dict) 
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Org id has no users and roles.")
            roles_details = sorted(roles_details, key=lambda x: x['role_master_id'], reverse=True) 
            return{"response":roles_details}
        finally:        
            db.close()

    def get_all_role_masters_data(self):
        db = next(get_db())
        try:
            roles_masters = db.query(Role_Master).all() 
            roles_details = [] 
            for role in roles_masters:
                role_dict = {
                    "role_master_id": role.role_master_id,
                    "role": role.role,
                    "role_description" : role.role_description,
                    "status": role.status
                }
                role_status = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == role.status).first()
                permissions_list = db.query(Role_Has_Permissions).filter(Role_Has_Permissions.role_id == role.role_master_id).all()
                role_dict["role_status"] = role_status.value
                role_dict["permissions_list"] = permissions_list
                roles_details.append(role_dict) 
            roles_details = sorted(roles_details, key=lambda x: x['role_master_id'], reverse=True) 
            return{"response":roles_details}
        finally:        
            db.close()

    # def roles_master_id(self,id,org_id):
    #     db = next(get_db())
    #     try:  
    #         roles_details = []
    #         roles_masters = db.query(Role_Master)\
    #         .join(User, User.role_id == id)\
    #         .filter(Role_Master.role_master_id == id).filter(User.org_id == org_id).first() 
    #         if roles_masters:
    #             role_dict = {
    #                 "role_master_id": roles_masters.role_master_id,
    #                 "role": roles_masters.role,
    #                 "role_description" : roles_masters.role_description,
    #                 "status": roles_masters.status
    #             }
    #             role_status = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == roles_masters.status).first()
    #             permissions_list = db.query(Role_Has_Permissions).filter(Role_Has_Permissions.role_id == roles_masters.role_master_id).all()
    #             role_dict["role_status"] = role_status.value
    #             role_dict["permissions_list"] = permissions_list
    #             roles_details.append(role_dict)
    #         else:
    #             raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Role id not found")    
    #         return{"response": roles_details} 
    #     finally:        
    #         db.close()
            
    def update_roles_masters(self,id,data):
        db = next(get_db())
        try:
            update_roles_masters = db.query(Role_Master).filter(Role_Master.role_master_id == id).first()
            if(update_roles_masters):
                update_roles_masters.role_description= data.role_description,
                update_roles_masters.updated_by_id = data.updated_by_id
                db.commit()
                if data.permissions:
                    existing_permissions = db.query(Role_Has_Permissions).filter(Role_Has_Permissions.role_id == update_roles_masters.role_master_id).all()
                    existing_permissions_set = set(permission.permissions_id for permission in existing_permissions)
                    new_permissions_set = set(data.permissions)
                    permissions_to_add = new_permissions_set - existing_permissions_set
                    permissions_to_remove = existing_permissions_set - new_permissions_set
                    for exist_permissions in existing_permissions:
                        exist_permissions.updated_by_id = data.updated_by_id
                        db.commit()
                    for permission in permissions_to_add:
                        new_role_permissions = Role_Has_Permissions(
                            role_id=update_roles_masters.role_master_id,
                            permissions_id=permission,
                            created_by_id=data.updated_by_id,
                            updated_by_id = data.updated_by_id
                        )
                        db.add(new_role_permissions)
                        db.commit()
                    for permission_id in permissions_to_remove:
                        db.query(Role_Has_Permissions).filter(
                            Role_Has_Permissions.role_id == update_roles_masters.role_master_id,
                            Role_Has_Permissions.permissions_id == permission_id
                        ).delete()
                        db.commit()
                    return{"response":"Role Master updated Successfully"}  
                else :
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="permissions are empty at least one permission should select")                        
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Role id not found")
        finally:        
            db.close()
    def change_roles_status(self,role_id,data):
        db = next(get_db())
        try:
            role = db.query(Role_Master).filter(Role_Master.role_master_id == role_id).first()
            active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
            inactive = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "0").first()
            
            if(role.status == active.miscellaneous_id):
                role.status = inactive.miscellaneous_id,
                role.updated_by_id = data.updated_by_id
                db.commit()
            elif(role.status == inactive.miscellaneous_id):
                role.status = active.miscellaneous_id,
                role.updated_by_id = data.updated_by_id
                db.commit()  
            return {"data" : "Role Status updated successfully"}
        finally:
            db.close()
# ----------------- permissions list code -------------------------------

class Permissions_Service:    
    def permissions_list(self):
        db = next(get_db())
        try:
            permissions_list = db.query(Permissions).all()
            permissions_dict = {}
            for permission in permissions_list:
                screen_name = permission.screen_name
                if screen_name not in ['Organization', 'Smo']:
                    if screen_name not in permissions_dict:
                        permissions_dict[screen_name] = []
                    permissions_dict[screen_name].append({
                        "permission_name": permission.permission_name,
                        "id": permission.id
                    })
            return permissions_dict
        finally:        
            db.close()