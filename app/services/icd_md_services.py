from app.model.icd_md import Icd_Md
# from app.model.specialities import Specialities
from app.model.icd import Icd
from app.model.site import Site
from app.db.database import get_db
from fastapi import HTTPException,status
from sqlalchemy import desc,text
from app.model.user import User


class  icd_md_data:
    def post_icd_data(self, data):
        db = next(get_db())
        success_messages = []
        error_messages = []      
        for icd_code in data.icd_code:
                icdcode = db.query(Icd_Md).filter(
                    Icd_Md.icd_code == icd_code.strip(),  # Trim any leading/trailing spaces
                    Icd_Md.site_id == data.site_id
                ).first()
                if icdcode:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Icd already exists for this Site")
                else:
                    try:
                        new_icd = Icd_Md(
                            site_id=data.site_id,
                            icd_code=icd_code.strip(),  # Trim any leading/trailing spaces
                            created_by_id=data.created_by_id
                        )
                        db.add(new_icd)
                        success_messages.append(f"Icd code {icd_code} added successfully")
                    except Exception as e:
                        error_messages.append("Icd is not added ")
        try:
            db.commit()
            return {
                "success_messages": success_messages
            }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()



    def get_icd_data_all(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()       
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]
        try:
            site_icds = db.query(Icd_Md).filter(Icd_Md.created_by_id.in_(user_ids)).order_by(desc(Icd_Md.created)).all()
            all_records=[]
            for record in site_icds:
                icd_id_codes = record.icd_code
                icd_id_list= icd_id_codes.split(':') 
                icd_main_record=[]
                site_record = db.query(Site).filter(Site.site_id==record.site_id).first()
                site_name = site_record.site_name
                site_code = site_record.site_code
                record.site_code = site_code
                record.site_name = site_name
                for id in icd_id_list:
                    id= int(id)
                    icd_record =db.query(Icd).filter(Icd.icd_id == id).first()
                    icd_main_record.append(icd_record)
                record.icd_main_record = icd_main_record
                


                all_records.append(record)
            return all_records
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
        finally:
            db.close()
        


    
    def get_delete_icd(self,id):
        db = next(get_db())
        try:
            icd_data = db.query(Icd_Md).filter(Icd_Md.icd_id == id).first()
            if(icd_data):
                db.delete(icd_data)
                db.commit()
                return{"successs":"deleted sucessfully"}
            else:
                return{"error":" Icd data is not deleted"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_icd_data(self,id):
        db = next(get_db())
        try:
            icd_codes = db.query(Icd_Md).filter(Icd_Md.site_id == id).first()
            icd_codesdecode = db.query(Icd_Md).filter(Icd_Md.site_id == id).all()
            all_records=[]
            data =[]
            site_record = db.query(Site).filter(Site.site_id==icd_codes.site_id).first()
            site_name = site_record.site_name
            site_code = site_record.site_code
            icd_codes.site_code = site_code
            icd_codes.site_name = site_name
            all_records.append(icd_codes)
            
            for recordseprated in icd_codesdecode:
                icd_id_codes = recordseprated.icd_code
                icd_id_list= icd_id_codes.split(':')
                icd_main_record=[]
                for id in icd_id_list:
                    id= int(id)
                    icd_record =db.query(Icd).filter(Icd.icd_id == id).first()
                    icd_main_record.append(icd_record)
                data.append(icd_main_record)
                icd_codes.icd_main_record = data
                # print(icd_main_record)
            return icd_codes 
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Site record does not exist ")
        finally:
            db.close()
