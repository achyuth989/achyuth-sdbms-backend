from app.model.site_equipment import Site_Equipment
from app.model.site import Site
from app.model.cities import City
from app.model.equipment_mapping import Equipment_Mapping
from app.model.equipment_type import Equipment_Type
from app.model.md_equipments_site import Md_Equipments_Site
from app.db.database import get_db
from sqlalchemy import and_ , func, or_
from fastapi import HTTPException, status
from app.model.user import User
from app.model.organizations import Organizations
from typing import List
from app.model.miscellaneous import Miscellaneous
import datetime
from sqlalchemy.sql.expression import exists
from sqlalchemy import desc,and_,text
from sqlalchemy.orm import joinedload,aliased

class Site_Equipments:
    def post_site_equipment(self,siteequipmentdetails):
        db = next(get_db())
        site_city = db.query(Site).filter(Site.site_id == siteequipmentdetails.site_id).first()
        # city_names = db.query(City).filter(City.city_id == site_city.city).first()
        equipment_mapping_md = db.query(Md_Equipments_Site)\
            .filter(Md_Equipments_Site.md_equipment_site_id == siteequipmentdetails.equipment_instrument_name)\
            .first()
        # check_equ = db.query(Site_Equipment)\
        #     .filter(Site_Equipment.md_equipment_site_id == siteequipmentdetails.equipment_instrument_name)\
        #     .first()
        check_equ = db.query(Site_Equipment)\
            .filter(Site_Equipment.site_equipment_id == siteequipmentdetails.equipment_id)\
            .first()
        try:
            if check_equ:
                check_equ.site_id = siteequipmentdetails.site_id,
                check_equ.md_equipment_site_id = equipment_mapping_md.md_equipment_site_id,
                check_equ.equipment_type = equipment_mapping_md.equipment_type,
                check_equ.equipment_instrument_name = equipment_mapping_md.equipment_name,
                check_equ.brand = siteequipmentdetails.brand,
                check_equ.model = siteequipmentdetails.model,
                check_equ.serial_number = siteequipmentdetails.serial_number,
                check_equ.capacity_range = siteequipmentdetails.capacity_range,
                # check_equ.site_location = city_names.city_name,
                check_equ.instrument_id = siteequipmentdetails.instrument_id,
                check_equ.last_maintenance_date = siteequipmentdetails.last_maintenance_date,
                check_equ.next_maintenance_date = siteequipmentdetails.next_maintenance_date,	
                check_equ.calibration_qualification = siteequipmentdetails.calibration_qualification,
                check_equ.validity = 	siteequipmentdetails.validity,	
                check_equ.remarks = siteequipmentdetails.remarks,
                check_equ.updated_by_id = siteequipmentdetails.created_by_id,
                db.commit()
                return {"details" : "Site equipment details updated successfully"}
            else:
                add_site_equ_details = Site_Equipment(
                    site_id = siteequipmentdetails.site_id,
                    md_equipment_site_id = equipment_mapping_md.md_equipment_site_id,
                    equipment_type = equipment_mapping_md.equipment_type,
                    equipment_instrument_name = equipment_mapping_md.equipment_name,
                    brand = siteequipmentdetails.brand,
                    model = siteequipmentdetails.model,
                    serial_number = siteequipmentdetails.serial_number,
                    capacity_range = siteequipmentdetails.capacity_range,
                    # site_location = city_names.city_name,
                    instrument_id = siteequipmentdetails.instrument_id,
                    last_maintenance_date = siteequipmentdetails.last_maintenance_date,			
                    next_maintenance_date = siteequipmentdetails.next_maintenance_date,	
                    calibration_qualification = siteequipmentdetails.calibration_qualification,
                    validity = 	siteequipmentdetails.validity,	
                    remarks = siteequipmentdetails.remarks,
                    created_by_id = siteequipmentdetails.created_by_id
                )
                db.add(add_site_equ_details)
                db.commit()
                db.refresh(add_site_equ_details)
                return {"details" : "Site equipment details added successfully"}
        finally:
            db.close()
    # def get_site_equipment_all(self):
    #     db= next(get_db())
    #     try:
    #         # equipment_details_all = db.query(Site_Equipment).all()
    #         equipment_details_all = db.query(Site_Equipment.site_equipment_id,
    #         Site_Equipment.site_id,Site_Equipment.md_equipment_site_id,Site_Equipment.equipment_type,
    #         Site_Equipment.equipment_instrument_name,Site_Equipment.brand,Site_Equipment.model,
    #         Site_Equipment.serial_number,Site_Equipment.capacity_range,
    #         Site_Equipment.instrument_id,Site_Equipment.last_maintenance_date,Site_Equipment.next_maintenance_date,
    #         Site_Equipment.calibration_qualification,Site_Equipment.validity,Site_Equipment.remarks,Site_Equipment.created_by_id,User.name,Site_Equipment.created,Site_Equipment.updated,Site_Equipment.updated_by_id,
    #         Site.site_code,Site.site_name,Equipment_Type.equipment_code,Equipment_Type.equipment_type_id)\
    #             .join(Site, Site.site_id == Site_Equipment.site_id)\
    #             .join(Equipment_Type, Equipment_Type.equipment_type == Site_Equipment.equipment_type)\
    #             .join(User,User.id == Site_Equipment.created_by_id)\
    #             .order_by(desc(Site_Equipment.created))\
    #             .all()            
    #         return {"siteequipment_details" : equipment_details_all}
    #     finally:
    #         db.close()    
    
    
    def get_site_equipment_all(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]       
        try:
            created_by_user = aliased(User, name="created_by_user")
            updated_by_user = aliased(User, name="updated_by_user")

            equipment_details_all = db.query(
                Site_Equipment.site_equipment_id,
                Site_Equipment.site_id,
                Site_Equipment.md_equipment_site_id,
                Site_Equipment.equipment_type,
                Site_Equipment.equipment_instrument_name,
                Site_Equipment.brand,
                Site_Equipment.model,
                Site_Equipment.serial_number,
                Site_Equipment.capacity_range,
                Site_Equipment.instrument_id,
                Site_Equipment.last_maintenance_date,
                Site_Equipment.next_maintenance_date,
                Site_Equipment.calibration_qualification,
                Site_Equipment.validity,
                Site_Equipment.remarks,
                Site_Equipment.created_by_id,
                created_by_user.name.label("created_by_name"),
                func.TO_CHAR(Site_Equipment.created, 'YYYY-MM-DD').label("formatted_created"),
                func.TO_CHAR(Site_Equipment.updated, 'YYYY-MM-DD').label("formatted_updated"),
                Site_Equipment.updated_by_id,
                updated_by_user.name.label("updated_by_name"),
                Site.site_code,
                Site.site_name,
                Equipment_Type.equipment_code,
                Equipment_Type.equipment_type_id
            ).join(Site, Site.site_id == Site_Equipment.site_id).join(
                Equipment_Type, Equipment_Type.equipment_type == Site_Equipment.equipment_type
            ).outerjoin(
                created_by_user, created_by_user.id == Site_Equipment.created_by_id
            ).outerjoin(
                updated_by_user, updated_by_user.id == Site_Equipment.updated_by_id
            ).filter((Site_Equipment.created_by_id.in_(user_ids))).order_by(desc(Site_Equipment.created)).all()
            
            return {"siteequipment_details": equipment_details_all}
        finally:
            db.close()               
            
    def get_site_equipment(self,site_id):
        db = next(get_db())
        try:
            equ_details = db.query(Site_Equipment.site_equipment_id,
            Site_Equipment.site_id,Site_Equipment.md_equipment_site_id,Site_Equipment.equipment_type,
            Site_Equipment.equipment_instrument_name,Site_Equipment.brand,Site_Equipment.model,
            Site_Equipment.serial_number,Site_Equipment.capacity_range,
            Site_Equipment.instrument_id,Site_Equipment.last_maintenance_date,Site_Equipment.next_maintenance_date,
            Site_Equipment.calibration_qualification,Site_Equipment.validity,Site_Equipment.remarks,
            Site.site_code,Site.site_name,Equipment_Type.equipment_code,Equipment_Type.equipment_type_id)\
                .join(Site, Site.site_id == Site_Equipment.site_id)\
                .join(Equipment_Type, Equipment_Type.equipment_type == Site_Equipment.equipment_type)\
                .filter(Site_Equipment.site_id == site_id)\
                .order_by(desc(Site_Equipment.created))\
                .all()
            return {"details" : equ_details}
        finally:
            db.close()
    def search_sites_status(self,site_id,site_status):
        db = next(get_db())
        try:
            if site_id and site_status :
                site_list = db.query(Site.site_id, Site.site_code, Site.site_name, Miscellaneous.value).join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.status).filter(and_(Site.site_id == site_id, Site.status == site_status)).all()
                return {"site_list" : site_list}
            if site_status :
                site_list = db.query(Site.site_id, Site.site_code, Site.site_name, Miscellaneous.value).join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.status).filter(Site.status == site_status).all()
                return {"site_list" : site_list}
            if site_id :
                site_list = db.query(Site.site_id, Site.site_code, Site.site_name, Miscellaneous.value).join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.status).filter(Site.site_id == site_id).all()
                return {"site_list" : site_list}
            else :
                return {"code": "fields are empty"}
        finally:
            db.close()     

    # def get_site_equip_status(self):
    #     db = next(get_db())
    #     try:
    #         sites = db.query(Site).with_entities(
    #             Site.site_id,
    #             Site.site_code,
    #             Site.site_name,
    #             exists().where(Site_Equipment.site_id == Site.site_id).label("has_equipment"),
    #         ).all()

    #         response = [
    #             {
    #                 "site_id": site.site_id,
    #                 "site_code": site.site_code,
    #                 "site_name": site.site_name,
    #                 "status": "Completed" if site.has_equipment else "Not started",
    #             }
    #             for site in sites
    #         ]
    #         return response

    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #     finally:
    #         db.close()
    
    def get_site_equip_status(self):
        db = next(get_db())
        active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
        sites = db.query(Site).filter(Site.status == active.miscellaneous_id).order_by(desc(Site.created)).all()
        try:
            response=[]
            for site in sites:
                equipment = db.query(Site_Equipment).filter(Site_Equipment.site_id == site.site_id).order_by(desc(Site_Equipment.created)).first()
                if(equipment):
                    status = "Completed"
                else:
                    status = "Not Started"
                data = {
                "site_id": site.site_id,
                "site_code":site.site_code,
                "site_name": site.site_name,
                "status": status
                }
                response.append(data)
            return response

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        finally:
            db.close() 
            
    def filter_site_equipment(self, data):
        db = next(get_db())
        try:
            site_id_list = data.site_id
            site_equipment_id = data.site_equipment_id
            md_equipment_site_id = data.md_equipment_site_id

            # Initialize the query with all equipment records
            query = db.query(Site_Equipment)

            # Filter by site_id values if provided
            if site_id_list and any(site_id != 0 for site_id in site_id_list):
                query = query.filter(Site_Equipment.site_id.in_(site_id_list))

            # Filter by site_equipment_id if provided
            if site_equipment_id > 0:
                query = query.filter(Site_Equipment.site_equipment_id == site_equipment_id)

            # Filter by md_equipment_site_id if provided
            if md_equipment_site_id > 0:
                query = query.filter(Site_Equipment.md_equipment_site_id == md_equipment_site_id)

            # Order the results
            query = query.order_by(desc(Site_Equipment.created))
            
            # Retrieve the filtered equipment records
            equipments = query.all()

            equipment_list = []
            for equipment in equipments:
                # Retrieve information for each equipment and build the equipment_list
                site = db.query(Site).filter(Site.site_id == equipment.site_id).first()

                md_equipment_site_id = db.query(Md_Equipments_Site).filter(
                    Md_Equipments_Site.md_equipment_site_id == equipment.md_equipment_site_id
                ).first()

                equipment_object = {
                    "site_equipment_id": equipment.site_equipment_id,
                    "site_id": equipment.site_id,
                    "site_code": site.site_code,
                    "md_equipment_site_id": equipment.md_equipment_site_id,
                    "equipment_type": md_equipment_site_id.equipment_type,
                    "equipment_instrument_name": md_equipment_site_id.equipment_name,
                    "brand": equipment.brand,
                    "model": equipment.model,
                    "serial_number": equipment.serial_number,
                    "capacity_range": equipment.capacity_range,
                    "instrument_id": equipment.instrument_id,
                    "last_maintenance_date": equipment.last_maintenance_date,
                    "next_maintenance_date": equipment.next_maintenance_date,
                    "calibration_qualification": equipment.calibration_qualification,
                    "validity": equipment.validity,
                    "remarks": equipment.remarks
                }
                equipment_list.append(equipment_object)
            return equipment_list

        finally:
            db.close()
  