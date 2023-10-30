from app.model.study_type import Study_Type
from app.db.database import get_db
from fastapi import HTTPException,status
from sqlalchemy import func,desc,asc
from app.model.user import User

class study_typess:
    def Study_Type(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_type_list = []
        for user in users:
            study_type = db.query(Study_Type).filter(Study_Type.created_by_id == user.id).all()
            if(study_type):
                existing_type_list.extend(study_type)
        check_existing_type = False
        if any(existing_type.study_type_id.lower() == data.study_type_id.lower() for existing_type in existing_type_list):
            check_existing_type = True
        # std_type = db.query(Study_Type).filter(func.lower(Study_Type.study_type_id) == data.study_type_id.lower()).first()
        if check_existing_type:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Study type already exist.")
        else:
            try:
                new_type = Study_Type(
                    study_type_id = data.study_type_id,
                    study_type = data.study_type,
                    description = data.description,
                    created_by_id = data.created_by_id
                )
                db.add(new_type)
                db.commit()
                return{"success":"successfully created the study type"}
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create study type.")
            finally:    
                db.close()         

    def get_study_type_all(self,user_id):
        db = next(get_db())
        try:
            
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    all_study_types_list =[]
                    for user in list_of_users_related_to_org:
                        std_types = db.query(Study_Type).filter(Study_Type.created_by_id == user.id).order_by((Study_Type.created)).all()
                        all_study_types_list.extend(std_types)
                    return all_study_types_list
                else:
                    return {"response":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"response":f"user_id = {user_id} not found"}            
            # std_types = db.query(Study_Type).order_by((Study_Type.created)).all()
            # return std_types
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_study_type_by_id(self,id):
        db = next(get_db())
        try:
            studytypes = db.query(Study_Type).filter(Study_Type.studytype_id == id).all()
            return studytypes
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_study_type(self,id,data):
        db = next(get_db())
        updatestudytypes = db.query(Study_Type).filter(Study_Type.studytype_id == id).first()
        try:
            if(updatestudytypes):

                updatestudytypes.study_type = data.study_type,
                updatestudytypes.description = data.description,
                updatestudytypes.updated_by_id = data.updated_by_id
                db.commit()
                return{"response":"Study Type updated successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Study Type not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()