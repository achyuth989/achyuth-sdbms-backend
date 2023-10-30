from app.db.database import get_db
from app.model.study_phases import StudyPhases
from fastapi import HTTPException, status
from sqlalchemy import func,desc,asc
from app.model.user import User

class Study_Phases_Service():
    def add_study_phases(self, study_phases_details):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == study_phases_details.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_phase_list = []
        for user in users:
            study_phases = db.query(StudyPhases).filter(StudyPhases.created_by_id == user.id).all()
            if(study_phases):
                existing_phase_list.extend(study_phases)
        check_existing_phase = False
        if any(existing_phase.phase_id.lower() == study_phases_details.phase_id.lower() for existing_phase in existing_phase_list):
            check_existing_phase = True
        # study_phase_id = db.query(StudyPhases).filter(func.lower(StudyPhases.phase_id) == study_phases_details.phase_id.lower()).first()
        if check_existing_phase:
            raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "Phase id already exist.")
        else:
            try:
                new_study_phase = StudyPhases(
                    phase_id = study_phases_details.phase_id,
                    phases_type = study_phases_details.phases_type,
                    description = study_phases_details.description,
                    created_by_id  = study_phases_details.created_by_id
                )
                db.add(new_study_phase)
                db.commit()
                db.refresh(new_study_phase)
                return {"success" : "Study phases added successfully."}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            finally :
                db.close()
    def study_phases_list(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    all_study_phases_list =[]
                    for user in list_of_users_related_to_org:
                        study_phase_list = db.query(StudyPhases).filter(StudyPhases.created_by_id == user.id).order_by((StudyPhases.created)).all()
                        all_study_phases_list.extend(study_phase_list)
                    return {"study_phases_list": all_study_phases_list}
                else:
                    return {"response":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"response":f"user_id = {user_id} not found"}
            # study_phase_list = db.query(StudyPhases).order_by((StudyPhases.created)).all()
            # return {"study_phases_list": study_phase_list}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_study_phases(self,id,data):
        db = next(get_db())
        studyphases = db.query(StudyPhases).filter(StudyPhases.study_phase_id == id).first()
        try:
            if(studyphases):
                studyphases.phases_type=data.phases_type,
                studyphases.description=data.description,
                studyphases.updated_by_id=data.updated_by_id
                db.commit()
                return{"response":"Study Phase Updated Successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Study phase not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_study_phase(self,id):
        db = next(get_db())
        try:
            study_phase_list = db.query(StudyPhases).filter(StudyPhases.study_phase_id == id).first()
            return {"study_phases_list": study_phase_list}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()    
