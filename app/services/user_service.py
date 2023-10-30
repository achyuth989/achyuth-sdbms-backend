from app.model.user import User
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db
from app.services.email_services import EmailService
from app.model.role_master import Role_Master
from app.model.miscellaneous import Miscellaneous
from sqlalchemy import desc, func
from app.model.organizations import Organizations
from app.model.permissions import Permissions
from app.model.role_has_permissions import Role_Has_Permissions
import pandas as pd
from datetime import datetime
class User_Service:
    def user_signin(self, user_login):
        db = next(get_db())
        try:
            if not user_login.email or not user_login.password:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing email or password")
            user = db.query(User).filter(User.email == user_login.email).order_by(User.id.desc()).first()
            user_status_pending = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(func.lower(Miscellaneous.value) == "pending").first()
            user_status_rejected = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(func.lower(Miscellaneous.value) == "rejected").first()
            role_status = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "0").first()
            if user:
                role = db.query(Role_Master).filter(Role_Master.role_master_id == user.role_id).first()
                if user.status == user_status_pending.miscellaneous_id :
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user status is still pending.")
                elif user.status == user_status_rejected.miscellaneous_id:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user status is rejected.")
                elif role.status == role_status.miscellaneous_id :
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user role is inactive.")
                else :
                    if bcrypt.checkpw(user_login.password.encode(), user.password.encode()):
                        permissions = db.query(Permissions).join(Role_Has_Permissions,Permissions.id == Role_Has_Permissions.permissions_id).filter(Role_Has_Permissions.role_id == user.role_id).all()
                        permissions_dict = {}
                        for permission in permissions:
                            main_feature = permission.screen_name
                            feature_name = permission.screen_type
                            permission_name = permission.permission_name
                            permission_id = permission.id

                            if main_feature not in permissions_dict:
                                permissions_dict[main_feature] = {
                                    "features": {}
                                }

                            if feature_name not in permissions_dict[main_feature]["features"]:
                                permissions_dict[main_feature]["features"][feature_name] = []

                            permissions_dict[main_feature]["features"][feature_name].append({
                                "permission_name": permission_name,
                                "permission_id": permission_id
                            })

                        permissions_list = []

                        for main_feature, data in permissions_dict.items():
                            permissions_list.append({
                                "main_feature": main_feature,
                                "features": [{"feature_name": k, "permissions": v} for k, v in data["features"].items()]
                            })
                        
                        return {
                            "id": user.id,
                            "email": user.email,
                            "role_id" : role.role_master_id if role else None,
                            "role": role.role if role else None,
                            "name": user.name, 
                            "created_by_id":user.created_by_id,
                            "created":user.created ,
                            "org_id" : user.org_id,
                            "permissions" :  permissions_list if permissions else []             
                        }
                    else:
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        finally:
            db.close()

    def user_signup(self,create_user):
        db = next(get_db())
        
        org_id =create_user.org_id 
        user_id = create_user.created_by_id
        if org_id == 0 or org_id is None:
            
            # get org_id of current user based on to which organisation he belongs to
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            if get_data_of_user:
                org_id = get_data_of_user.org_id
                # if get_data_of_user.org_id:
                #     get_list_of_users_related_to_org_except_current_user = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                #     return get_list_of_users_related_to_org_except_current_user
        else:
            org_id =create_user.org_id 
            
        existing_email = db.query(User).filter(func.lower(User.email) == create_user.email.lower()).first()
        if(existing_email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Exists")

        # email_service = EmailService()
        # random_password = email_service.random_passcode(8)
        # password =random_password.encode()
        # hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        # hashed_password = hashed_password.decode('utf-8')
        user_status = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(func.lower(Miscellaneous.value) == create_user.status.lower()).first()
        try:
            new_user = User(
                # password=hashed_password,
                email=create_user.email,
                role_id=create_user.role_id,
                name=create_user.name,
                status = user_status.miscellaneous_id,
                created_by_id = create_user.created_by_id,
                org_id = org_id
            )
            db.add(new_user)
            db.commit()

            # to_email = create_user.email
            # user_name = create_user.name
            # user_password = random_password
            # email_service.send_email(to_email,user_name,user_password)
            db.refresh(new_user)
            return {"detail": "User registered successfully."}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    # def get_user_role(self, user_role):
    #     db = next(get_db())
    #     try:
    #         # if not user_role:
    #         #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing email or password")
    #         user = db.query(User).filter(User.role == user_role).all()
    #         if user:
    #             return  {"detail": user }
    #         else:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    #     except HTTPException as e:
    #         raise
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    #     finally:
    #         db.close()

    def get_users(self):
        db = next(get_db())
        try:
            users = db.query(User.email,User.id,User.name,Role_Master.role_master_id, Role_Master.role,Miscellaneous.miscellaneous_id,Miscellaneous.value).outerjoin(Role_Master, Role_Master.role_master_id == User.role_id).outerjoin(Miscellaneous, Miscellaneous.miscellaneous_id == User.status).order_by(desc(User.created)).all()
            return users 
        finally:
            db.close() 

    def get_user(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            
            if get_data_of_user:
                if get_data_of_user.org_id:
                    get_list_of_smo_admins_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).order_by(desc(User.created)).all()
                    # added order by created timestamp in descending order
                    # Exclude the current user's data from the list
                    final_users_list = [user for user in get_list_of_smo_admins_related_to_org if user.id != user_id]

                    
                    
                    # return get_list_of_smo_admins_related_to_org
                    # final_users_list = []
                    # for user in get_list_of_smo_admins_related_to_org:
                        
                    #     users_data = db.query(User).filter(User.created_by_id == user.id).all()

                    #     final_users_list.extend(users_data)

                    if final_users_list:
                        for user in final_users_list:
                            if user.name is not None and user.name.strip() != "":
                                user.name = user.name.title().strip()
                            else:
                                user.name = None

                            
                            role_data = db.query(Role_Master).filter(Role_Master.role_master_id== user.role_id).first()
                            if role_data:
                                if role_data.role is not None and role_data.role.strip() != "":
                                    user.role_name = role_data.role
                                else:
                                    user.role_name = None
                            else:
                                user.role_name = None
                             
                             
                            org_data = db.query(Organizations).filter(Organizations.id== user.org_id).first()
                            if org_data:
                                if org_data.org_name is not None and org_data.org_name.strip() != "":
                                    user.org_name = org_data.org_name.strip().title()
                                else:
                                    user.org_name = None
                            else:
                                user.org_name = None
                                
                                
                            status_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id== user.status).first()
                            if status_data:
                                if status_data.value is not None and status_data.value.strip() != "":
                                    if status_data.value == "0":
                                        user.user_status = "Inactive"
                                    else:
                                        user.user_status = status_data.value.title().strip()
                                else:
                                    user.user_status = None
                            else:
                                user.user_status = None
                                
                    
                        return final_users_list
                else:
                    return {"response":"No data found"}
            else:
                return {"response":"No valid data"}
                        
            # user = db.query(User.email,User.id,User.name,Role_Master.role_master_id, Role_Master.role,Miscellaneous.miscellaneous_id,Miscellaneous.value).outerjoin(Role_Master, Role_Master.role_master_id == User.role_id).outerjoin(Miscellaneous, Miscellaneous.miscellaneous_id == User.status).filter(User.id == id).all()
            # return user
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()     

    def user_update(self,id,data):
        db=next(get_db())
        user = db.query(User).filter(User.id == id).first()
        user_status = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(func.lower(Miscellaneous.value) == data.status.lower()).first()
        user_status_approved = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(func.lower(Miscellaneous.value) == "approved").first()
        try:
            if(user):
                # default_password = None
                email_service = EmailService()
                random_password = email_service.random_passcode(8)
                password =random_password.encode()
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                hashed_password = hashed_password.decode('utf-8')

                if data.status.lower() == "approved" and user.status != user_status_approved.miscellaneous_id :
                    # default_password = hashed_password
                    user.password = hashed_password
                    to_email = user.email
                    user_name = user.name
                    user_password = random_password
                    email_service.send_email(to_email,user_name,user_password)

                
                user.role_id = data.role_id
                user.status = user_status.miscellaneous_id
                user.updated_by_id = data.updated_by_id
                db.commit()
                # if user_status_approved.miscellaneous_id == user.status :
                    
                return "User Updated Successfully"
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        finally:
            db.close()        

        # -----------------------------------------------------get all smo-admins---------------------------------------------

    def get_smo_admins(self):
        db = next(get_db())
        try:
            smo_admin_role_data = db.query(Role_Master).filter(func.lower(Role_Master.role) == "smo-admin").first()
            if smo_admin_role_data:
                smo_admin_data = db.query(User).filter(User.role_id==smo_admin_role_data.role_master_id).order_by(desc(User.created)).all()
                
                for data in smo_admin_data:
                    
                    if smo_admin_role_data.role is not None and smo_admin_role_data.role.strip() !="": 
                        data.role = smo_admin_role_data.role.title().strip()
                    else: 
                        data.role = None
                        
                    organisation_id = data.org_id 

                
                    if organisation_id:
                        org_data = db.query(Organizations).filter(Organizations.id==data.org_id).first()
                        
                        if org_data:
                            organisation_name = org_data.org_name.title().strip()
                        else:
                            organisation_name = None
                        
                        data.org_name = organisation_name
                    else:
                        data.org_name = None
                     
                    user_status = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.status).first()
                    if user_status.value is not None and user_status.value.strip() != "":
                        if user_status.value == "0":
                            data.user_status = "Inactive"
                        else:
                            data.user_status = user_status.value.title().strip()
                        
                    else:
                        data.user_status = None
                    
                    if data.name is not None and data.name.strip() != "":
                        data.name = data.name.title().strip()
                    else:
                        data.name = None
                        
                        
                    
                return smo_admin_data
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
    
    # --------------------------------------toggle user status approved or inactive-------------------
    def update_user_status_by_id(self,data):
        db = next(get_db())
        try:
            user_data = db.query(User).filter(User.id == data.id).first()
            
            active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(func.lower(Miscellaneous.value) == "approved").first()
            inactive = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(func.lower(Miscellaneous.value) == "0").first()
            if(user_data.status == active.miscellaneous_id):
                user_data.status = inactive.miscellaneous_id
                user_data.updated_by_id = data.updated_by_id
                db.commit()
                return {"response":"user deactivated succesfully"}
            elif(user_data.status == inactive.miscellaneous_id):
                user_data.status = active.miscellaneous_id
                user_data.updated_by_id = data.updated_by_id
                db.commit()
                return {"response":"user activated succesfully"}
            else:
                return {"response":f"status not found for this users table = {user_data.id}"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def multiple_users_upload(self, file_path: str,id,org_id):
        db = next(get_db())
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                # print("Csv Data:")
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
                # print("Excel Data:")
                # print(df)
            elif file_path.endswith('.xls'):
                df = pd.read_excel(file_path)  
                # print("Excel Data:")
                # print(df)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format") 
            if df.empty:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
                        
            error_messages = []
            new_user_added = False 

            for index, row in df.iterrows():
                user_details = {
                    "name": row["name"],
                    "email": row["email"]    
                }
                                
                existing_user = db.query(User).filter(
                    func.lower(User.email) == str(user_details['email']).lower()
                ).first()
                if existing_user:
                    error_messages.append(f"User email '{user_details['email']}' already exists for {existing_user.name}.")                       
                else:
                    # Create a new user record
                    # email_service = EmailService()
                    # random_password = email_service.random_passcode(8)
                    # password =random_password.encode()
                    # hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                    # hashed_password = hashed_password.decode('utf-8')
                    user_status = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(func.lower(Miscellaneous.value) == "pending").first()
                    new_user = User(
                        # password=hashed_password,
                        email=user_details["email"],
                        name=user_details["name"],
                        status = user_status.miscellaneous_id, 
                        org_id = org_id,
                        created_by_id=id,
                        created=datetime.now()
                    )
                   
                    db.add(new_user)
                    db.commit()
                    # to_email = user_details["email"]
                    # user_name = user_details["name"]
                    # user_password = random_password
                    # email_service.send_email(to_email,user_name,user_password)
                    db.refresh(new_user)
                    new_user_added = True
            if new_user_added:
                return {"message": "Data uploaded and processed successfully, new Users added."}
            else:
                raise HTTPException(status_code=400, detail="No new Users were added.")
        finally:
            db.close()