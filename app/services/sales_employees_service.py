from app.model.sales_employees import SalesEmployees
from fastapi import HTTPException, status,FastAPI, UploadFile, File
from app.db.database import get_db 
from typing import List,Dict 
from typing import List,Dict 
from sqlalchemy import func,desc,create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session 
import os
import pandas as pd
from sqlalchemy import func,desc
from app.model.department import Department
from datetime import datetime
from fastapi.responses import JSONResponse
from app.model.user import User

class Sales_Employees_Service:
    def process_uploaded_file(self, file_path: str,id):
        db = next(get_db())
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                print("Csv Data:")
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
                print("Excel Data:")
                print(df)
            elif file_path.endswith('.xls'):
                df = pd.read_excel(file_path)  
                print("Excel Data:")
                print(df)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format") 
            if df.empty:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
                        

            departments = db.query(Department).all()
            department_mapping = {}            

            for department in departments:
                department_mapping[department.department_name] = department.department_id
            error_messages = []
            new_employee_added = False 

            for index, row in df.iterrows():
                emp_details = {
                    "employee_code": row["employee_code"],
                    "employee_name": row["employee_name"],
                    "role": row["role"],
                    "start_date": (
                        row["start_date"].strftime("%Y-%m-%d")
                        if isinstance(row["start_date"], pd.Timestamp)
                        else datetime.strptime(row["start_date"], "%d-%m-%Y").strftime("%Y-%m-%d")
                    ),
                    "end_date": (
                        row["end_date"].strftime("%Y-%m-%d")
                        if isinstance(row["end_date"], pd.Timestamp)
                        else datetime.strptime(row["end_date"], "%d-%m-%Y").strftime("%Y-%m-%d")
                    ),
                    "department": row["department"]
                    
                }
                print(f"Processing row: {emp_details}")
                department_names = emp_details['department'].strip().split(",") if emp_details['department'] else []
                department_ids = []
                department_error_messages = []
                
                for department_name in department_names:
                    department_id = department_mapping.get(department_name.strip())
                    print(f"department----->", department_name)
                    if department_id:
                        department_ids.append(department_id)
                        print(f"department_id:{department_ids}")
                    else:
                        raise HTTPException(status_code=400, detail="department does not exist")
                    

                # Fetch the department based on the department name
                department_name = emp_details["department"].strip()
                department = db.query(Department).filter(Department.department_name == department_name).first()
                
                existing_employee = db.query(SalesEmployees).filter(
                    func.lower(SalesEmployees.employee_code) == emp_details['employee_code'].lower()
                ).first()
                if existing_employee:
                    error_messages.append(f"Employee code '{emp_details['employee_code']}' already exists for {existing_employee.employee_name}.")                   
                    # error_messages.append(f"Employee code '{emp_details['employee_code']}' already exists.")
                    
                else:
                    # Create a new employee record
                    new_emp = SalesEmployees(
                        employee_code=emp_details["employee_code"],
                        employee_name=emp_details["employee_name"],
                        role=emp_details["role"],
                        start_date=emp_details["start_date"],
                        end_date=emp_details["end_date"],
                        created_by_id=id
                    )
                    if department:
                        new_emp.department = department_ids
                    print(f"New employee added: {new_emp.employee_code}")
                    db.add(new_emp)
                    db.commit()
                    db.refresh(new_emp)
                    new_employee_added = True
           

            if new_employee_added:
                return {"message": "Data uploaded and processed successfully, new employees added."}
            else:
                raise HTTPException(status_code=400, detail="No new employees were added.")
            
            if error_messages:
                response_content = {"error_messages": error_messages}
                return JSONResponse(content=response_content, status_code=400)
                # return {"error_messages": error_messages}
        except HTTPException as e:
            raise e  
        except Exception as e:
            db.rollback()
            error_message = "An error occurred during processing: " + str(e)
            raise HTTPException(status_code=500, detail=error_message)
        finally:
            db.close()

    def add_sales_employee(self, emp_details):
        db = next(get_db())

        org_id = db.query(User).filter(User.id == emp_details.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_employee_list = []
        for user in users:
            employees = db.query(SalesEmployees).filter(SalesEmployees.created_by_id == user.id).all()
            if(employees):
                existing_employee_list.extend(employees)
        check_existing_employee = False
        if any(existing_employee.employee_code.lower() == emp_details.employee_code.lower() for existing_employee in existing_employee_list):
            check_existing_employee = True        
        
        # emp_id = db.query(SalesEmployees).filter(func.lower(SalesEmployees.employee_code) == emp_details.employee_code.lower()).first()
        if check_existing_employee:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Employee code already exist.")
        else:
            try:
                new_emp = SalesEmployees(
                    employee_code  = emp_details.employee_code,
                    employee_name  = emp_details.employee_name,
                    role  = emp_details.role,
                    start_date  = emp_details.start_date,
                    end_date 	= emp_details.end_date,
                    department = emp_details.department,
                    created_by_id  = emp_details.created_by_id
                )
                print(emp_details.department)
                db.add(new_emp)
                db.commit()
                db.refresh(new_emp)
                return {"success": "Sales employee added successfully."}
            # except Exception as e:
            #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            finally:
                db.close()
    def sales_employees_list(self,user_id):
        db = next(get_db())
        try:
            # sales_emp_list = db.query(SalesEmployees.sales_employee_id,SalesEmployees.employee_name,SalesEmployees.role, SalesEmployees.start_date, SalesEmployees.end_date,Department.department_id, Department.department_code, Department.department_name).outerjoin(Department, Department.department_id == SalesEmployees.department).order_by(desc(SalesEmployees.created)).all()
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    all_sales_emoloyees =[]
                    for user in list_of_users_related_to_org:
                        
                        sales_emp_list = db.query(SalesEmployees).filter(SalesEmployees.created_by_id == user.id).order_by(desc(SalesEmployees.created)).all()
                        emp_list =[]
                        for employee in sales_emp_list:
                            employee_id = db.query(SalesEmployees).filter(SalesEmployees.sales_employee_id == employee.sales_employee_id).first()
                            emp_object = {
                                "sales_employee_id":employee_id.sales_employee_id,
                                "employee_code":employee_id.employee_code,
                                "employee_name": employee_id.employee_name,
                                "role": employee_id.role,
                                "start_date": employee_id.start_date,
                                "end_date": employee_id.end_date
                            }
                            department = db.query(SalesEmployees.department).filter(SalesEmployees.sales_employee_id == employee.sales_employee_id).first()
                            print(department[0])
                            department_list =[]
                            for department in department[0]:
                                department_object = db.query(Department.department_id, Department.department_code, Department.department_name).filter(Department.department_id == department).first()
                                department_list.append(department_object)
                            emp_object['departments'] = department_list    
                            emp_list.append(emp_object)
                        all_sales_emoloyees.extend(emp_list)  
                        
                    return all_sales_emoloyees
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}    

        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def sales_employee_details(self, id):
        db = next(get_db())
        sales_emp = db.query(SalesEmployees).filter(SalesEmployees.sales_employee_id == id).first()
        emp_object = {
                "sales_employee_id":sales_emp.sales_employee_id,
                "employee_code":sales_emp.employee_code,
                "employee_name": sales_emp.employee_name,
                "role": sales_emp.role,
                "start_date": sales_emp.start_date,
                "end_date": sales_emp.end_date
            }
        department_list =[]
        for department in sales_emp.department:
            department_object = db.query(Department.department_id, Department.department_code, Department.department_name).filter(Department.department_id == department).first()
            department_list.append(department_object)
        emp_object['departments'] = department_list
        try:
            if sales_emp:
                return emp_object
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sales id not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
    def update_employee_details(self, id, sales_emp_details):
        db = next(get_db())
        sales_emp_detail = db.query(SalesEmployees).filter(SalesEmployees.sales_employee_id == id).first()
        try:
            if sales_emp_detail:
                sales_emp_detail.employee_name  = sales_emp_details.employee_name
                sales_emp_detail.role  = sales_emp_details.role
                sales_emp_detail.start_date  = sales_emp_details.start_date
                sales_emp_detail.end_date     = sales_emp_details.end_date
                sales_emp_detail.department = sales_emp_details.department
                sales_emp_detail.updated_by_id = sales_emp_details.updated_by_id
                db.commit()
                return {"success": "Sales employee updated successfully."}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sales id not found.")   
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()    