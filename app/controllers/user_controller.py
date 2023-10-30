from typing import List
from fastapi import APIRouter, Depends, UploadFile
from app.schemas.user import User, UserLogin, UpdateUser,User_Status_Schema
from app.services.user_service import User_Service
import os
router = APIRouter(prefix="/api")
user_service = User_Service()

@router.post("/signin")
def user_signin(user_login: UserLogin):
    response  =  user_service.user_signin(user_login)
    return response

@router.post("/users")
def user_signup(create_user: User):
    response  =  user_service.user_signup(create_user)
    return response

# @router.post("/user/{user_role}")
# def user_signup(user_role: str):
#     response  =  user_service.get_user_role(user_role)
#     return response

@router.get("/users")
def get_users():
    response  =  user_service.get_users()
    return response 

@router.get("/users/{user_id}")
def get_users_corresponding_to_smo_admin(user_id:int):
    response  =  user_service.get_user(user_id)
    return response        

@router.put("/users/{id}")
def user_update(id:int,data: UpdateUser):
    response  =  user_service.user_update(id,data)
    return response    

@router.get("/get-smo-admins")
def get_all_smo_admins():
    response = user_service.get_smo_admins()
    return response

@router.put("/update-user-status")
def update_user_status(data:User_Status_Schema):
    response = user_service.update_user_status_by_id(data)
    return response

def is_valid_file(filename: str):
        return filename.endswith(('.csv', '.xlsx','.xls'))
    
    
def save_uploaded_file(file: UploadFile):
        filename = os.path.basename(file.filename)
        os.makedirs("temp", exist_ok=True)
        temp_file_path = os.path.join("temp", filename)

        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.file.read())        
        return temp_file_path
    
@router.post("/multiple-users-upload/{id}/{org_id}")
async def upload_file(file: UploadFile, id:int, org_id:int):
    if not is_valid_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # Save the uploaded file to a temporary location
    temp_file_path = save_uploaded_file(file)
    print("Temporary file path:", temp_file_path)
    response = user_service.multiple_users_upload(temp_file_path,id,org_id)
    return response
    # except Exception as e:
    #     logger.error("Error occurred during processing:", exc_info=True)
    #     print("Error:", str(e))
    #     return {"error": "Error occurred while uploading and processing the data"}