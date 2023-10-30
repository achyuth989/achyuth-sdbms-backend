from app.model.cr import Cr
from fastapi import HTTPException, status
import bcrypt
from fastapi.logger import logger
from app.db.database import get_db
from datetime import datetime
from app.model.cr_roles import Cr_Roles
from app.model.cr_roles import Cr_Roles
from app.model.study_phases import StudyPhases
from app.model.miscellaneous import Miscellaneous
from app.model.upload_documents import Upload_Documents
from app.model.cr_status import Cr_Status


class Cr_Service:
    def post_cr(self, add_cr_list):
        db = next(get_db())
        try:
            site_ids = [add_cr.site_id for add_cr in add_cr_list.Cr_List]
            existing_site_ids = db.query(Cr.site_id).filter(Cr.site_id.in_(site_ids)).all()
            existing_site_ids = [site_id for (site_id,) in existing_site_ids]
            if existing_site_ids:
                return {"response": f"CRs with site_id {existing_site_ids} already exist"}
            for add_cr in add_cr_list.Cr_List:
                new_cr = Cr(
                    site_id=add_cr.site_id,
                    cr_code=add_cr.cr_code,
                    salutation=add_cr.salutation,
                    first_name=add_cr.first_name,
                    last_name=add_cr.last_name,
                    speciality=add_cr.speciality,
                    cr_experience=add_cr.cr_experience,
                    clinical_phases=add_cr.clinical_phases,
                    certificate_of_good_clinical_practice=add_cr.certificate_of_good_clinical_practice,
                    role=add_cr.role,
                    cv_available=add_cr.cv_available,
                    cr_status = add_cr.cr_status,
                    created_by_id=add_cr.created_by_id,
                    created=datetime.now()
                )
                db.add(new_cr)
            db.commit()
            return {"response": "CRs added successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def get_cr_by_id(self, site_id):
        db = next(get_db())
        try:
            cr_data = db.query(Cr).filter(Cr.site_id == site_id).all()
            for data in cr_data:
                cr_role_data = db.query(Cr_Roles).filter(Cr_Roles.cr_role_id == data.role).first()
                # study_data = db.query(StudyPhases).filter(StudyPhases.study_phase_id == data.clinical_phases).first()
                miscellaneous_data1 = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.cr_experience).first()
                miscellaneous_data2 = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.certificate_of_good_clinical_practice).first()
                miscellaneous_data3 = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.cv_available).first()
                uploaddocument = db.query(Upload_Documents).filter(Upload_Documents.cr_code == data.site_rec_cr_id, Upload_Documents.site_id == data.site_id).first()
                cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == data.cr_status).first()
                if(uploaddocument):
                    status = "Completed"
                else:
                    status = "Not Started"
                if cr_role_data is not None:
                    data.cr_role = cr_role_data.cr_role
                    data.cr_id = cr_role_data.cr_id
                    # data.type = study_data.study_phase_id
                    # data.value = study_data.phases_type
                    data.cr_experience_value=miscellaneous_data1.value
                    data.certificate_of_good_clinical_practice_value=miscellaneous_data2.value
                    data.cv_available_value=miscellaneous_data3.value
                    data.upload_doc_cr_status = status
                    data.cr_status_value = cr_status.cr_status
            return cr_data
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def get_cr(self):
        db = next(get_db())
        try:
            cr_data = db.query(Cr).all()
            for data in cr_data:
                cr_role_data = db.query(Cr_Roles).filter(Cr_Roles.cr_role_id == data.role).first()
                # study_data = db.query(StudyPhases).filter(StudyPhases.study_phase_id == data.clinical_phases).first()
                miscellaneous_data1 = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.cr_experience).first()
                miscellaneous_data2 = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.certificate_of_good_clinical_practice).first()
                miscellaneous_data3 = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == data.cv_available).first()
                if cr_role_data is not None:
                    data.cr_role = cr_role_data.cr_role
                    data.cr_id = cr_role_data.cr_id
                    # data.study_phase_id = data.clinical_phases
                    # data.phases_type = study_data.phases_type
                    data.cr_experience_value=miscellaneous_data1.value
                    data.certificate_of_good_clinical_practice_value=miscellaneous_data2.value
                    data.cv_available_value=miscellaneous_data3.value
            return cr_data
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def update_cr(self, site_id, update_cr_list):
        db = next(get_db())
        try:
            for update_cr in update_cr_list.Cr_List:
                existing_cr = db.query(Cr).filter(Cr.site_rec_cr_id == update_cr.site_rec_cr_id).first()
                if not existing_cr:
                    new_cr = Cr(
                        site_id=site_id,
                        # site_rec_cr_id=update_cr.site_rec_cr_id,
                        created_by_id=update_cr.updated_by_id,  # Assuming created_by_id is set to updated_by_id
                        created=datetime.now(),  # Assuming created is set to updated
                        updated_by_id=update_cr.updated_by_id,
                        updated=datetime.now(),
                        cr_code=update_cr.cr_code,
                        salutation=update_cr.salutation,
                        first_name=update_cr.first_name,
                        last_name=update_cr.last_name,
                        speciality=update_cr.speciality,
                        cr_experience=update_cr.cr_experience,
                        certificate_of_good_clinical_practice=update_cr.certificate_of_good_clinical_practice,
                        role=update_cr.role,
                        clinical_phases=update_cr.clinical_phases,
                        cv_available=update_cr.cv_available,
                        cr_status = update_cr.cr_status
                    )
                    db.add(new_cr)
                else:
                    existing_cr.site_id = site_id
                    existing_cr.cr_code = update_cr.cr_code
                    existing_cr.salutation = update_cr.salutation
                    existing_cr.first_name = update_cr.first_name
                    existing_cr.last_name = update_cr.last_name
                    existing_cr.speciality = update_cr.speciality
                    existing_cr.cr_experience = update_cr.cr_experience
                    existing_cr.certificate_of_good_clinical_practice = update_cr.certificate_of_good_clinical_practice
                    existing_cr.role = update_cr.role
                    existing_cr.clinical_phases = update_cr.clinical_phases
                    existing_cr.cv_available = update_cr.cv_available
                    existing_cr.cr_status = update_cr.cr_status
                    existing_cr.updated_by_id = update_cr.updated_by_id
                    existing_cr.updated = datetime.now()
    
            db.commit()
            return {"response": "CRs updated successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        finally:
            db.close()
    
    def delete_cr(self,id):
        db = next(get_db())
        try:
            cr = db.query(Cr).filter(Cr.site_rec_cr_id == id).first()
            db.delete(cr)
            db.commit()
            return "CR deleted Successfully"
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        finally:
            db.close()    
