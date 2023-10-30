from app.model.department import Department
from fastapi import HTTPException, status
from app.db.database import get_db
from sqlalchemy import func,desc
from app.model.user import User

class Department_service():
    def add_department(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_department_list = []
        for user in users:
            departments = db.query(Department).filter(Department.created_by_id == user.id).all()
            if(departments):
                existing_department_list.extend(departments)
        check_existing_department = False
        if any(existing_department.department_code.lower() == data.department_code.lower() for existing_department in existing_department_list):
            check_existing_department = True        
        # department_id = db.query(Department).filter(func.lower(Department.department_code) == data.department_code.lower()).first()
        if check_existing_department:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=" department already exist.")
        else:
            try:
                new_department = Department(
                    department_code = data.department_code,
                    department_name = data.department_name,
                    created_by_id = data.created_by_id
                )
                db.add(new_department)
                db.commit()
                db.refresh(new_department)
                return{"success" : "Successfully added department"}
            # except Exception as e:
            #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            finally:
                db.close()
    
    def department_list(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    departments =[]
                    for user in list_of_users_related_to_org:
                        department_list = db.query(Department).filter(Department.created_by_id == user.id).order_by(desc(Department.created)).all()
                        departments.extend(department_list)
                    return{"department_list":departments}
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
            
    def update_department(self,id,data):
        db= next(get_db())
        updatedepartment = db.query(Department).filter(Department.department_id == id).first()
        try:
            if(updatedepartment):
                updatedepartment.department_name = data.department_name,
                updatedepartment.updated_by_id = data.updated_by_id
                db.commit()
                return{"success":"department updated sucessfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="department not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
    def get_all_departments(self,id):
        db= next(get_db())
        try:
            departments_list = db.query(Department).filter(Department.department_id == id).first()
            return {"department_list": departments_list}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
            

