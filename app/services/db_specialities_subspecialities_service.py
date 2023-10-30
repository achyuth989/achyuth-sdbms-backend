from app.model.user import User
from app.model.speciality_subspeciality import SpecialitySubspeciality
from app.model.speciality import Speciality
from app.model.db_specialities_subspecialities import Specialities_Subspecialities
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc,not_,asc

class Db_Specialities_Subspecialities_Service:
    def get_all_specialities(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    added_spec_sub_specs =[]
                    for user in list_of_users_related_to_org:
                        specialities = db.query(Specialities_Subspecialities.specialities_subspecialities_id,SpecialitySubspeciality.speciality_id,SpecialitySubspeciality.subspeciality,Speciality.speciality).join(SpecialitySubspeciality,Specialities_Subspecialities.spec_sub_id == SpecialitySubspeciality.id ).join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id ).filter(Specialities_Subspecialities.created_by_id==user.id).order_by(desc(Specialities_Subspecialities.created)).all()
                        # doc_category_list = db.query(DocumentCategory).filter(DocumentCategory.created_by_id==user.id).order_by(desc(DocumentCategory.created)).all()
                        added_spec_sub_specs.extend(specialities)
                    return added_spec_sub_specs
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}

            # specialities = db.query(Specialities_Subspecialities.specialities_subspecialities_id,SpecialitySubspeciality.speciality_id,SpecialitySubspeciality.subspeciality,Speciality.speciality).join(SpecialitySubspeciality,Specialities_Subspecialities.spec_sub_id == SpecialitySubspeciality.id ).join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id ).order_by(desc(Specialities_Subspecialities.created)).all()
            # return specialities
        finally:
            db.close()    
    def get_specialities(self,id):
        db = next(get_db())
        try:
            specialities = db.query(Specialities_Subspecialities.specialities_subspecialities_id,SpecialitySubspeciality.speciality_id,SpecialitySubspeciality.subspeciality,Speciality.speciality).join(SpecialitySubspeciality,Specialities_Subspecialities.spec_sub_id == SpecialitySubspeciality.id ).join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id ).filter(Specialities_Subspecialities.specialities_subspecialities_id == id).first()
            return specialities
        finally:
            db.close() 
  
    def add_specialities(self, data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_speciality_list = []
        for user in users:
            specialities = db.query(Specialities_Subspecialities).filter(Specialities_Subspecialities.created_by_id == user.id).all()
            if(specialities):
                existing_speciality_list.extend(specialities)
        check_existing_speciality = False
        for speciality in data.speciality_ids[0]:  
            if any(existing_speciality.spec_sub_id == int(speciality) for existing_speciality in existing_speciality_list):
                check_existing_speciality = True
                break 
        try:
            speciality_list = []
            existing_ids = [] 
            spec_len = len(data.speciality_ids)
            
            if(spec_len == 1):
                spec_id = db.query(Specialities_Subspecialities).filter(Specialities_Subspecialities.spec_sub_id == data.speciality_ids[0]).first()
                if(check_existing_speciality):
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Speciality & SubSpeciality already exists")
                else:
                    new_speciality = Specialities_Subspecialities(
                        spec_sub_id=data.speciality_ids[0],
                        created_by_id=data.created_by_id
                    )
                    db.add(new_speciality)
                    db.commit()
                    return "Speciality & SubSpeciality added Successfully"

            else:    
                for speciality in data.speciality_ids:
                    speciality_id = db.query(Specialities_Subspecialities).filter(Specialities_Subspecialities.spec_sub_id == speciality).first()
                    if speciality_id:
                        existing_ids.append(speciality_id.spec_sub_id)  
                        continue 
                        
                    new_speciality = Specialities_Subspecialities(
                        spec_sub_id=speciality,
                        created_by_id=data.created_by_id
                    )
                    speciality_list.append(new_speciality)
                
                if speciality_list:
                    db.add_all(speciality_list)
                    db.commit()
                    for spec in speciality_list:
                        db.refresh(spec)
                existing_array = {}        
                for id in existing_ids:
                    existing_speciality = db.query(Specialities_Subspecialities.specialities_subspecialities_id,SpecialitySubspeciality.subspeciality,Speciality.speciality).join(SpecialitySubspeciality,Specialities_Subspecialities.spec_sub_id == SpecialitySubspeciality.id ).join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id ).filter(Specialities_Subspecialities.specialities_subspecialities_id == id).first()        
                    existing_array[id]= existing_speciality
                    
                if existing_ids:
                    return {"response": "Speciality & SubSpeciality added Successfully", "existing_ids": existing_array}
                else:
                    return {"response": "Speciality & SubSpeciality added Successfully"}
        finally:
            db.close()

    def get_specialities_list(self,user_id):
        db = next(get_db())
        try:
            org_id = db.query(User).filter(User.id == user_id).first()
            users = db.query(User).filter(User.org_id == org_id.org_id).all()
            existing_speciality_list = []
            for user in users:
                specialities = db.query(Specialities_Subspecialities).filter(Specialities_Subspecialities.created_by_id == user.id).all()
                if(specialities):
                    existing_speciality_list.extend(specialities)

            results = db.query(SpecialitySubspeciality.id, Speciality.speciality, SpecialitySubspeciality.subspeciality).join(Speciality).all()
            db_specialities = db.query(Specialities_Subspecialities.spec_sub_id).all()
            spec_sub_ids_to_remove = {item.spec_sub_id for item in existing_speciality_list}

            filtered_results = [item for item in results if item["id"] not in spec_sub_ids_to_remove]

            return filtered_results
        finally:
            db.close()    