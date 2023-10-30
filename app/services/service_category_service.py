from  app.model.service_category import Service_Category
from fastapi import HTTPException,status
from app.db.database import get_db 
from sqlalchemy import func,desc
from app.model.miscellaneous import Miscellaneous
from app.model.user import User


class Service_Categories:
    def  Service_Category_Service(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_category_list = []
        for user in users:
            categories = db.query(Service_Category).filter(Service_Category.created_by_id == user.id).all()
            if(categories):
                existing_category_list.extend(categories)
        check_existing_category = False
        if any(existing_category.service_category.lower() == data.service_category.lower() for existing_category in existing_category_list):
            check_existing_category = True  
        # services_cat = db.query(Service_Category).filter(func.lower(Service_Category.service_category) == data.service_category.lower()).first()
        if check_existing_category:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="service category  already exist.")
        else:
            try:
                indicator = db.query(Miscellaneous).filter(Miscellaneous.type == "indicator").filter(func.lower(Miscellaneous.value) == data.indicator.lower()).first()
                
                new_service = Service_Category(
                    service_category=data.service_category,
                    description=data.description,
                    service_category_indicator = indicator.miscellaneous_id,
                    created_by_id=data.created_by_id,
                )
                db.add(new_service)
                db.commit()
                return {"message":"service category created"}
            # except Exception as e:
            #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add service category.")
            finally:
                db.close()

    def get_Service_Category_all(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    service_category_list =[]
                    for user in list_of_users_related_to_org:
                        categories = db.query(Service_Category.service_category, Service_Category.service_category_indicator, Service_Category.service_category_id, Service_Category.description,Miscellaneous.value).outerjoin(Miscellaneous,Miscellaneous.miscellaneous_id == Service_Category.service_category_indicator).filter(Service_Category.created_by_id == user.id).order_by(desc(Service_Category.created)).all()
                        service_category_list.extend(categories)
                    return service_category_list
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_Service_Category_by_id(self,id):
        db = next(get_db())
        try:
            categories = db.query(Service_Category.service_category, Service_Category.service_category_indicator, Service_Category.service_category_id, Service_Category.description,Miscellaneous.value).outerjoin(Miscellaneous,Miscellaneous.miscellaneous_id == Service_Category.service_category_indicator).filter(Service_Category.service_category_id == id).all()
            return categories
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_service_category(self,id,data):
        db = next(get_db())
        servicecategories = db.query(Service_Category).filter(Service_Category.service_category_id == id).first()
        try:
            indicator = db.query(Miscellaneous).filter(Miscellaneous.type == "indicator").filter(func.lower(Miscellaneous.value) == data.indicator.lower()).first()
            if(servicecategories):
                servicecategories.description=data.description,
                servicecategories.service_category_indicator = indicator.miscellaneous_id,
                servicecategories.updated_by_id=data.updated_by_id
                db.commit()
                return{"response":"Service Category is updated sucessfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service category not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()