from app.model.user import User
from app.model.equipment_mapping import Equipment_Mapping
from app.model.equipment_type import Equipment_Type
from app.model.md_equipments_site import Md_Equipments_Site
from app.model.miscellaneous import Miscellaneous
from app.model.site import Site
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc,and_ 

class Md_Equipments_Site_Service:
    def add_equipment(self,data):
        db = next(get_db())
        try:
            if data.equipment_name :  
                for equipment in data.equipment_name:
                    equipment_list = [int(num) for num in equipment.split(",")]
                    for equipments in equipment_list:
                        equipment_mapping = db.query(Equipment_Mapping.equipment_mapping_id, Equipment_Mapping.equipment_type_id, Equipment_Mapping.equipment_name, Equipment_Type.equipment_code, Equipment_Type.equipment_type, Equipment_Type.equipment_description)\
                            .join(Equipment_Type, Equipment_Type.equipment_type_id == data.equipment_type)\
                            .filter(Equipment_Mapping.equipment_mapping_id == equipments)\
                            .first()
                        miscellaneous_list = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "1")).first()
                        add_equ = db.query(Md_Equipments_Site)\
                        .filter(Md_Equipments_Site.equipment_mapping_id == equipment_mapping.equipment_mapping_id)\
                        .filter(Md_Equipments_Site.site_id == data.site_id)\
                        .all()
                        if equipment_mapping:
                            if add_equ:
                                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="equipment id already exists")
                            else:
                                new_equipment = Md_Equipments_Site(
                                    site_id=data.site_id,
                                    equipment_mapping_id=equipment_mapping.equipment_mapping_id,
                                    equipment_type=equipment_mapping.equipment_type,
                                    equipment_name=equipment_mapping.equipment_name,
                                    status = miscellaneous_list.miscellaneous_id,
                                    created_by_id=data.created_by_id
                                )
                                db.add(new_equipment)
                                db.commit()
                                db.refresh(new_equipment)
                return {"equipments": "equipment added successfully"}
            else :
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="equipment name is empty.")
        finally:        
            db.close()

    def get_equipment(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()       
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]
        try:
            equipment_mapping = db.query(Md_Equipments_Site.md_equipment_site_id,Md_Equipments_Site.site_id,Md_Equipments_Site.equipment_mapping_id,Md_Equipments_Site.equipment_type,Md_Equipments_Site.equipment_name,Md_Equipments_Site.created_by_id,Miscellaneous.value, Site.site_code,Site.site_name,Equipment_Type.equipment_code)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Md_Equipments_Site.status)\
            .join(Equipment_Type, Equipment_Type.equipment_type == Md_Equipments_Site.equipment_type)\
            .join(Site, Site.site_id == Md_Equipments_Site.site_id)\
            .filter(Md_Equipments_Site.created_by_id.in_(user_ids))\
            .order_by(desc(Md_Equipments_Site.created))\
            .all()
            return{"response":equipment_mapping}
        finally:
            db.close()

    def get_equipment_by_id(self,id):
        db = next(get_db())
        try:
            equipment_mapping = db.query(Md_Equipments_Site.md_equipment_site_id,Md_Equipments_Site.site_id,Md_Equipments_Site.equipment_mapping_id,Md_Equipments_Site.equipment_type,Md_Equipments_Site.equipment_name,Miscellaneous.value, Site.site_code,Site.site_name,Equipment_Type.equipment_code)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Md_Equipments_Site.status)\
            .join(Equipment_Type, Equipment_Type.equipment_type == Md_Equipments_Site.equipment_type)\
            .join(Site, Site.site_id == Md_Equipments_Site.site_id)\
            .filter(Md_Equipments_Site.md_equipment_site_id == id)\
            .all()
            return{"response":equipment_mapping}
        finally:
            db.close()

    def status_equipment(self,id,data):
        db = next(get_db())
        equipment_mapping = db.query(Md_Equipments_Site)\
            .filter(Md_Equipments_Site.md_equipment_site_id == id)\
            .first()
        miscellaneous_active = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "1")).first()
        miscellaneous_inactive = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "0")).first()
        try:
            if (equipment_mapping):
                if(equipment_mapping.status == miscellaneous_active.miscellaneous_id):
                    equipment_mapping.status = miscellaneous_inactive.miscellaneous_id,
                    equipment_mapping.updated_by_id = data.updated_by_id
                    db.commit()
                elif(equipment_mapping.status == miscellaneous_inactive.miscellaneous_id):
                    equipment_mapping.status = miscellaneous_active.miscellaneous_id,
                    equipment_mapping.updated_by_id = data.updated_by_id
                    db.commit()
                return {"response":"Equipment mapping status updated Successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "equipment id not found")
        finally:
            db.close()   
    def get_equipment_by_site_id(self,site_id):
        db = next(get_db())
        miscellaneous_active = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "1")).first()
        try:
            equipment_mapping = db.query(Md_Equipments_Site.md_equipment_site_id,Md_Equipments_Site.site_id,Md_Equipments_Site.equipment_type,Md_Equipments_Site.equipment_name,Miscellaneous.value, Site.site_code,Site.site_name,Equipment_Type.equipment_code, Equipment_Type.equipment_type_id, Equipment_Type.equipment_description)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Md_Equipments_Site.status)\
            .join(Site, Site.site_id == Md_Equipments_Site.site_id)\
            .join(Equipment_Type, Equipment_Type.equipment_type == Md_Equipments_Site.equipment_type)\
            .filter(Md_Equipments_Site.site_id == site_id)\
            .filter(Md_Equipments_Site.status == miscellaneous_active.miscellaneous_id)\
            .all()
            return{"response":equipment_mapping}
        finally:
            db.close()
    def get_equipment_by_site_id_distinct(self,site_id):
        db = next(get_db())
        miscellaneous_active = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "1")).first()
        try:
            equipment_mapping = db.query(Md_Equipments_Site.md_equipment_site_id,Md_Equipments_Site.site_id,Md_Equipments_Site.equipment_type,Md_Equipments_Site.equipment_name,Miscellaneous.value, Site.site_code,Site.site_name,Equipment_Type.equipment_code, Equipment_Type.equipment_type_id, Equipment_Type.equipment_description)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Md_Equipments_Site.status)\
            .join(Site, Site.site_id == Md_Equipments_Site.site_id)\
            .join(Equipment_Type, Equipment_Type.equipment_type == Md_Equipments_Site.equipment_type)\
            .filter(Md_Equipments_Site.site_id == site_id)\
            .filter(Md_Equipments_Site.status == miscellaneous_active.miscellaneous_id)\
            .distinct(Md_Equipments_Site.equipment_type)\
            .all()
            return{"response":equipment_mapping}
        finally:
            db.close()
    def get_equipment_names_by_site_id(self,site_id,id):
        db = next(get_db())
        miscellaneous_active = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "1")).first()
        try:
            equ_type = db.query(Equipment_Type).filter(Equipment_Type.equipment_type_id == id).first()
            equ_names = db.query(Md_Equipments_Site)\
                .filter(Md_Equipments_Site.equipment_type == equ_type.equipment_type)\
                .filter(Md_Equipments_Site.site_id == site_id)\
                .filter(Md_Equipments_Site.status == miscellaneous_active.miscellaneous_id)\
                .all()
            return equ_names
        finally:
            db.close()
            
    # def get_equipment_type_names(self,equip_type_id):
    #     db= next(get_db())
    #     miscellaneous_active = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "1")).first()
    #     try:
    #         equ_type = db.query(Equipment_Type).filter(Equipment_Type.equipment_type_id == equip_type_id).first()
    #         equ_names = db.query(Md_Equipments_Site)\
    #             .filter(Md_Equipments_Site.equipment_type == equ_type.equipment_type)\
    #             .filter(Md_Equipments_Site.status == miscellaneous_active.miscellaneous_id)\
    #             .all()
    #         return equ_names
    #     finally:
    #         db.close()

 
    def get_equipment_type_names(self,equip_type_id):
        db= next(get_db())
        miscellaneous_active = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "1")).first()
        try:
            equ_type = db.query(Equipment_Type).filter(Equipment_Type.equipment_type_id == equip_type_id).first()
            equ_names = db.query(Md_Equipments_Site)\
                .filter(Md_Equipments_Site.equipment_type == equ_type.equipment_type)\
                .filter(Md_Equipments_Site.status == miscellaneous_active.miscellaneous_id)\
                .all()
            return equ_names
        finally:
            db.close()

   
