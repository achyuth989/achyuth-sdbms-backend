from app.model.user import User
from app.model.equipment_mapping import Equipment_Mapping
from app.model.equipment_type import Equipment_Type
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc

class Equipment_Mapping_Service:
    def add_equipment_mapping(self,data):
        db = next(get_db())
        try:   
            new_equipment_mapping = Equipment_Mapping(
                equipment_type_id = data.equipment_type_id,
                equipment_name = data.equipment_name,
                created_by_id = data.created_by_id
            )
            db.add(new_equipment_mapping)
            db.commit()
            db.refresh(new_equipment_mapping)
            return{"response":"Equipment Mapping added Successfully"}
        finally:        
            db.close()

    def get_equipment_mapping(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    added_document_mapping =[]
                    for user in list_of_users_related_to_org:
                        equipment_mapping = db.query(Equipment_Mapping.equipment_mapping_id, Equipment_Mapping.equipment_type_id, Equipment_Mapping.equipment_name, Equipment_Type.equipment_code, Equipment_Type.equipment_type, Equipment_Type.equipment_description)\
                            .join(Equipment_Type, Equipment_Type.equipment_type_id == Equipment_Mapping.equipment_type_id)\
                            .filter(Equipment_Mapping.created_by_id==user.id)\
                            .order_by(desc(Equipment_Mapping.created))\
                            .all()
                        # doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.created_by_id==user.id).order_by(desc(DocumentCategory.created)).all()
                        added_document_mapping.extend(equipment_mapping)
                    return {"response":added_document_mapping}
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}
            
            # equipment_mapping = db.query(Equipment_Mapping.equipment_mapping_id, Equipment_Mapping.equipment_type_id, Equipment_Mapping.equipment_name, Equipment_Type.equipment_code, Equipment_Type.equipment_type, Equipment_Type.equipment_description)\
            #     .join(Equipment_Type, Equipment_Type.equipment_type_id == Equipment_Mapping.equipment_type_id)\
            #     .order_by(desc(Equipment_Mapping.created))\
            #     .all()
            # return{"response":equipment_mapping}
        finally:
            db.close()

    def equipment_mapping(self,id):
        db = next(get_db())
        try:
            equipment_mapping = db.query(Equipment_Mapping.equipment_mapping_id, Equipment_Mapping.equipment_type_id, Equipment_Mapping.equipment_name, Equipment_Type.equipment_code, Equipment_Type.equipment_type, Equipment_Type.equipment_description)\
                .join(Equipment_Type, Equipment_Type.equipment_type_id == Equipment_Mapping.equipment_type_id)\
                .filter(Equipment_Mapping.equipment_mapping_id == id)\
                .all()
            return{"response":equipment_mapping}
        finally:
            db.close()

    def update_equipment_mapping(self,id,data):
        db = next(get_db())
        equipment_mapping = db.query(Equipment_Mapping).filter(Equipment_Mapping.equipment_mapping_id == id).first()
        try:
            if(equipment_mapping):
                equipment_mapping.equipment_type_id = data.equipment_type_id,
                equipment_mapping.equipment_name = data.equipment_name,
                equipment_mapping.updated_by_id = data.updated_by_id
                db.commit()
                return {"response":"Equipment mapping updated Successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Equipment mapping not found")
        finally:
            db.close()
    def get_equipment_names(self, id):
        db = next(get_db())
        try:
            equipment_names = db.query(Equipment_Mapping).filter(Equipment_Mapping.equipment_type_id == id).all()
            if equipment_names :
                return {"equipment" : equipment_names}
            else :
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Equipment type id not found")
        finally:
            db.close()   