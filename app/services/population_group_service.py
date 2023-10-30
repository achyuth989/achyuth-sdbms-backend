from app.model.user import User
from app.model.population_group import Population_Group
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc

class Population_Group_Service:
    def add_population_group(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_group_list = []
        for user in users:
            population_group = db.query(Population_Group).filter(Population_Group.created_by_id == user.id).all()
            if(population_group):
                existing_group_list.extend(population_group)
        check_existing_group = False
        if any(existing_group.population_group_id.lower() == data.population_group_id.lower() for existing_group in existing_group_list):
            check_existing_group = True
        try:
            # population_group_id = db.query(Population_Group).filter(func.lower(Population_Group.population_group_id) == data.population_group_id.lower()).first()
            if(check_existing_group):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="population group id already exists")
            else:    
                new_population_group = Population_Group(
                    population_group_id = data.population_group_id,
                    population_group_description = data.population_group_description,
                    created_by_id = data.created_by_id
                )
                db.add(new_population_group)
                db.commit()
                db.refresh(new_population_group)
                return{"response":"Population Group added Successfully"}
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:        
            db.close()

    def get_population_groups(self,user_id):
        db = next(get_db())
        try:

            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    added_population_grp =[]
                    for user in list_of_users_related_to_org:
                        population_groups = db.query(Population_Group).filter(Population_Group.created_by_id==user.id).order_by(desc(Population_Group.created)).all()
                        # doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.created_by_id==user.id).order_by(desc(DocumentCategory.created)).all()
                        added_population_grp.extend(population_groups)
                    return {"response":added_population_grp} 
                else:
                    return {"response":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"response":f"user_id = {user_id} not found"}
            

            # population_groups = db.query(Population_Group).order_by(desc(Population_Group.created)).all()
            # return{"response":population_groups}    
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_population_group(self,id):
        db = next(get_db())
        try:
            population_group = db.query(Population_Group).filter(Population_Group.population_group_served_id == id).all()
            return{"response":population_group}  
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()  

    def update_population_group(self,id,data):
        db = next(get_db())
        population_group = db.query(Population_Group).filter(Population_Group.population_group_served_id == id).first()
        try:
            if (population_group):
                population_group.population_group_description = data.population_group_description,
                population_group.updated_by_id = data.updated_by_id
                db.commit()
                return{"response": "Population group updated Successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Population group not found")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()