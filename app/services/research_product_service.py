from app.model.user import User
from app.model.research_product import Research_Product
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc

class Research_Product_Service:
    def add_research_product(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_product_list = []
        for user in users:
            research_product = db.query(Research_Product).filter(Research_Product.created_by_id == user.id).all()
            if(research_product):
                existing_product_list.extend(research_product)
        check_existing_product = False
        if any(existing_product.product_id.lower() == data.product_id.lower() for existing_product in existing_product_list):
            check_existing_product = True
        # product_id = db.query(Research_Product).filter(func.lower(Research_Product.product_id) == data.product_id.lower()).first()
        try:
            if(check_existing_product):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="product id already exists")
            else:    
                new_research_product = Research_Product(
                    product_id = data.product_id,
                    research_product_type = data.research_product_type,
                    product_description = data.product_description,
                    created_by_id = data.created_by_id
                )
                db.add(new_research_product)
                db.commit()
                db.refresh(new_research_product)
                return{"response":"Research Product added Successfully"}
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:       
            db.close()

    def get_research_product(self,user_id):
        db = next(get_db())
        try:
            
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    research_product_list =[]
                    for user in list_of_users_related_to_org:
                        research_product = db.query(Research_Product).filter(Research_Product.created_by_id == user.id).order_by(desc(Research_Product.created)).all()
                        research_product_list.extend(research_product)
                    return {"response":research_product_list}  
                else:
                    return {"response":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"response":f"user_id = {user_id} not found"}
            
            # research_product = db.query(Research_Product).order_by(desc(Research_Product.created)).all()
            # return{"response":research_product}   
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close() 

    def research_product(self,id):
        db = next(get_db())
        try:
            research_product = db.query(Research_Product).filter(Research_Product.research_product_id == id).all()
            return{"response":research_product} 
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_research_product(self,id,data):
        db = next(get_db())
        research_product = db.query(Research_Product).filter(Research_Product.research_product_id == id).first()
        try:
            if(research_product):
                research_product.research_product_type = data.research_product_type,
                research_product.product_description = data.product_description,
                research_product.updated_by_id = data.updated_by_id
                db.commit()
                return{"response":"Research product updated Successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Research product not found")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()