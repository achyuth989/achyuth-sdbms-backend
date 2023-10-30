from app.model.user import User
from app.model.equipment_type import Equipment_Type
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc

class Equipment_Type_Service:
    def add_equipment_type(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_equipment_list = []
        for user in users:
            equipment_type = db.query(Equipment_Type).filter(Equipment_Type.created_by_id == user.id).all()
            if(equipment_type):
                existing_equipment_list.extend(equipment_type)
        check_existing_equipment = False
        if any(existing_equipment.equipment_code.lower() == data.equipment_code.lower() for existing_equipment in existing_equipment_list):
            check_existing_equipment = True
        try:
            # equipment_id = db.query(Equipment_Type).filter(func.lower(Equipment_Type.equipment_code) == data.equipment_code.lower()).first()
            # equipment_type = db.query(Equipment_Type).filter(func.lower(Equipment_Type.equipment_type) == data.equipment_type.lower()).first()
            if(check_existing_equipment):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="equipment id already exists")
            # if(equipment_type):
            #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="equipment type already exists")
            else:    
                new_equipment_type = Equipment_Type(
                    equipment_code = data.equipment_code,
                    equipment_type = data.equipment_type,
                    equipment_description = data.equipment_description,
                    created_by_id = data.created_by_id
                )
                db.add(new_equipment_type)
                db.commit()
                db.refresh(new_equipment_type)
                return{"response":"Equipment type added Successfully"}
        finally:        
            db.close()

    def get_equipment_types(self):
        db = next(get_db())
        try:
            equipment_type = db.query(Equipment_Type).order_by(desc(Equipment_Type.created)).all()
            return{"response":equipment_type}    
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def equipment_type(self,id):
        db = next(get_db())
        try:
            equipment_type = db.query(Equipment_Type).filter(Equipment_Type.equipment_type_id == id).all()
            return{"response":equipment_type}    
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_equipment_type(self,id,data):
        db = next(get_db())
        equipment_type = db.query(Equipment_Type).filter(Equipment_Type.equipment_type_id == id).first()
        try:
            if(equipment_type):
                equipment_type.equipment_description = data.equipment_description,
                equipment_type.updated_by_id = data.updated_by_id
                db.commit()
                return {"response":"Equipment type updated Successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Equipment type not found")
        finally:
            db.close()