# from app.model.specialities import Specialities
from app.model.icd import Icd
from app.db.database import get_db
from fastapi import HTTPException,status

class SpecilaitiesSubspecialities:
    def get_specialities(self,data):
        db = next(get_db())
        try:
            new_specil = Specialities(
                icd_code=data.icd_code,
                therapeutic_area=data.therapeutic_area,
                sub_therapeutic_area=data.sub_therapeutic_area,
                created_by_id=data.created_by_id
            )
            db.add(new_specil)
            db.commit()
            return{"specialities  added sucessfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create Specialities and Subspecialities .")
        finally:    
            db.close()

    def get_specialities_all(self):
        db = next(get_db())
        specialities = db.query(Specialities).all()
        try:
            all_specialities=[]
            for speciality in specialities:
                icd_idd = db.query(Icd).filter(Icd.icd_id == speciality.icd_code).first()
                icd_des = db.query(Icd).filter(Icd.icd_id == speciality.icd_code).first()
                therapeutic_area_des = db.query(Icd).filter(Icd.icd_id == speciality.therapeutic_area).first()
                sub_therapeutic_area_des = db.query(Icd).filter(Icd.icd_id == speciality.sub_therapeutic_area).first()

                icd_id = icd_idd.icd_id
                icd_description = icd_des.icd_code
                therapeutic_area_description = therapeutic_area_des.description
                sub_therapeutic_area_description = sub_therapeutic_area_des.description

                speciality.icd_id =icd_id
                speciality.icd_description= icd_description
                speciality.therapeutic_area_description= therapeutic_area_description
                speciality.sub_therapeutic_area_description= sub_therapeutic_area_description
                all_specialities.append(speciality)
            return specialities  
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
 
    def get_specialities_id(self,id):
        db = next(get_db())
        specialities = db.query(Specialities).filter(Specialities.specialities_subspecialities_id == id).all()
        return specialities
        try:
            specialities = db.query(Specialities).filter(Specialities.specialities_subspecialities_id == id).all()
            return specialities
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
    
    def put_spcialities(self,id,data):
        db = next(get_db())
        specialities = db.query(Specialities).filter(Specialities.specialities_subspecialities_id == id).first()
        try:
            if(specialities):
                specialities.icd_code = data.icd_code,
                specialities.therapeutic_area = data.therapeutic_area,
                specialities.sub_therapeutic_area = data.sub_therapeutic_area,
                specialities.updated_by_id = data.updated_by_id,
                db.commit()
                return {"response":"Specialities updated sucessfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Specialities  not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
