from app.model.user import User
from app.model.site_assess_review import Site_Assess_Review
from app.model.miscellaneous import Miscellaneous
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc,not_,asc

class Site_Assess_Review_Service:
    def add_site_assess_review(self,data):
        db = next(get_db())
        existed_site = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_id == data.site_id).first()
        if(existed_site):
            return{"response":"Review data already saved for this Site"}
        else:    
            try:
                # reviewer_list = []
                # reviewer_type = "Reviewer Details"
                # for reviewer in data.reviewer_details:
                #     new_reviewer = Site_Assess_Review(
                #         site_id = data.site_id,
                #         date = reviewer.date,
                #         salutation = reviewer.salutation,
                #         first_name = reviewer.first_name,
                #         last_name = reviewer.last_name,
                #         role = reviewer.role,
                #         contact_phone = reviewer.contact_phone,
                #         contact_email = reviewer.contact_email,
                #         review_type = reviewer_type,
                #         created_by_id = data.created_by_id
                #     )
                #     reviewer_list.append(new_reviewer)
                # db.add_all(reviewer_list)     
                # db.commit() 
                # for reviewer in reviewer_list:
                #     db.refresh(reviewer)

                # user_department_list = []
                # user_department = "User Department"
                # for user in data.user_department:
                #     new_user = Site_Assess_Review(
                #         site_id = data.site_id,
                #         date = user.date,
                #         salutation = user.salutation,
                #         first_name = user.first_name,
                #         last_name = user.last_name,
                #         role = user.role,
                #         contact_phone = user.contact_phone,
                #         contact_email = user.contact_email,
                #         review_type = user_department,
                #         created_by_id = data.created_by_id
                #     )
                #     user_department_list.append(new_user)
                # db.add_all(user_department_list)     
                # db.commit() 
                # for user in user_department_list:
                #     db.refresh(user)

                # user_quality_list = []
                # user_quality = "Quality Assurance"
                # for user in data.quality_assurance:
                #     new_quality_user = Site_Assess_Review(
                #         site_id = data.site_id,
                #         date = user.date,
                #         salutation = user.salutation,
                #         first_name = user.first_name,
                #         last_name = user.last_name,
                #         role = user.role,
                #         contact_phone = user.contact_phone,
                #         contact_email = user.contact_email,
                #         review_type = user_quality,
                #         created_by_id = data.created_by_id
                #     )
                #     user_quality_list.append(new_quality_user)
                # db.add_all(user_quality_list)     
                # db.commit() 
                # for user in user_quality_list:
                #     db.refresh(user)  

                new_evaluation_mode = Site_Assess_Review(
                    site_id = data.site_id,
                    evaluation_mode = data.evaluation_mode,
                    created_by_id = data.created_by_id
                )
                db.add(new_evaluation_mode)
                db.commit()          
                return{"response":"review data added successfully"}
            finally:
                db.close()        
    def get_evalutation_modes(self):
        db = next(get_db())
        try:
            evaluation_modes = db.query(Miscellaneous).filter(Miscellaneous.type == "Evaluation Mode").all()
            return evaluation_modes 
        finally:
            db.close()    

    def get_site_assess_review(self,id):
        db = next(get_db())
        site_id = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_id == id).first()
        if(site_id):
            try:
                evaluation_modes = db.query(Site_Assess_Review.evaluation_mode).filter(Site_Assess_Review.site_id == id).filter(Site_Assess_Review.evaluation_mode != "").all()
                # reviewer_details = db.query(Site_Assess_Review.site_asmt_reviewer_id,Site_Assess_Review.date,Site_Assess_Review.salutation,Site_Assess_Review.first_name,Site_Assess_Review.last_name,Site_Assess_Review.role,Site_Assess_Review.contact_phone,Site_Assess_Review.contact_email).filter(Site_Assess_Review.site_id == id).filter(Site_Assess_Review.review_type == "Reviewer Details").all()
                # user_department = db.query(Site_Assess_Review.site_asmt_reviewer_id,Site_Assess_Review.date,Site_Assess_Review.salutation,Site_Assess_Review.first_name,Site_Assess_Review.last_name,Site_Assess_Review.role,Site_Assess_Review.contact_phone,Site_Assess_Review.contact_email).filter(Site_Assess_Review.site_id == id).filter(Site_Assess_Review.review_type == "User Department").all()
                # quality_assurance = db.query(Site_Assess_Review.site_asmt_reviewer_id,Site_Assess_Review.date,Site_Assess_Review.salutation,Site_Assess_Review.first_name,Site_Assess_Review.last_name,Site_Assess_Review.role,Site_Assess_Review.contact_phone,Site_Assess_Review.contact_email).filter(Site_Assess_Review.site_id == id).filter(Site_Assess_Review.review_type == "Quality Assurance").all()

                review_details = {}
                review_details['evaluation_modes']=evaluation_modes
                # review_details['reviewer_details']=reviewer_details
                # review_details['user_department']=user_department
                # review_details['quality_assurance']=quality_assurance
                return review_details
            
            finally:
                db.close()      
        else:
            return []       

    def update_site_assess_review(self,id,data):
        db = next(get_db())
        try:
            evaluation_modes = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_id == id).filter(Site_Assess_Review.evaluation_mode != "").first()
            if(evaluation_modes):
                evaluation_modes.evaluation_mode = data.evaluation_mode
                evaluation_modes.updated_by_id = data.updated_by_id
            else:
                new_evaluation_mode = Site_Assess_Review(
                    site_id = id,
                    evaluation_mode = data.evaluation_mode,
                    created_by_id = data.updated_by_id
                )
                db.add(new_evaluation_mode)
            db.commit()
            return{"response":"Review Details Updated Successfully"} 
        finally:
            db.close()
                # db.commit()    

            # reviewer_details = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_id == id).filter(Site_Assess_Review.review_type == "Reviewer Details").all()

            # spec_count = 0
            # for reviewer in data.reviewer_details:
            #     if spec_count < len(reviewer_details):
            #         reviewer_details[spec_count].date = reviewer.date
            #         reviewer_details[spec_count].salutation = reviewer.salutation
            #         reviewer_details[spec_count].first_name = reviewer.first_name
            #         reviewer_details[spec_count].last_name = reviewer.last_name
            #         reviewer_details[spec_count].role = reviewer.role
            #         reviewer_details[spec_count].contact_phone = reviewer.contact_phone
            #         reviewer_details[spec_count].contact_email = reviewer.contact_email
            #         reviewer_details[spec_count].updated_by_id = data.updated_by_id

            #     else:
            #         reviewer_type = "Reviewer Details"
            #         new_reviewer = Site_Assess_Review(
            #             site_id = id,
            #             date = reviewer.date,
            #             salutation = reviewer.salutation,
            #             first_name = reviewer.first_name,
            #             last_name = reviewer.last_name,
            #             role = reviewer.role,
            #             contact_phone = reviewer.contact_phone,
            #             contact_email = reviewer.contact_email,
            #             review_type = reviewer_type,
            #             created_by_id = data.updated_by_id
            #         )
            #         db.add(new_reviewer)
            #     spec_count += 1

            # db.commit()

            # user_department = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_id == id).filter(Site_Assess_Review.review_type == "User Department").all()

            # user_count = 0
            # for user in data.user_department:
            #     if user_count < len(user_department):
            #         user_department[user_count].date = user.date
            #         user_department[user_count].salutation = user.salutation
            #         user_department[user_count].first_name = user.first_name
            #         user_department[user_count].last_name = user.last_name
            #         user_department[user_count].role = user.role
            #         user_department[user_count].contact_phone = user.contact_phone
            #         user_department[user_count].contact_email = user.contact_email
            #         user_department[user_count].updated_by_id = data.updated_by_id

            #     else:
            #         user_department = "User Department"
            #         new_user = Site_Assess_Review(
            #             site_id = id,
            #             date = user.date,
            #             salutation = user.salutation,
            #             first_name = user.first_name,
            #             last_name = user.last_name,
            #             role = user.role,
            #             contact_phone = user.contact_phone,
            #             contact_email = user.contact_email,
            #             review_type = user_department,
            #             created_by_id = data.updated_by_id
            #         )
            #         db.add(new_user)
            #     user_count += 1

            # db.commit()

            # quality_assurance = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_id == id).filter(Site_Assess_Review.review_type == "Quality Assurance").all()

            # quality_count = 0
            # for quality in data.quality_assurance:
            #     if quality_count < len(quality_assurance):
            #         quality_assurance[quality_count].date = quality.date
            #         quality_assurance[quality_count].salutation = quality.salutation
            #         quality_assurance[quality_count].first_name = quality.first_name
            #         quality_assurance[quality_count].last_name = quality.last_name
            #         quality_assurance[quality_count].role = quality.role
            #         quality_assurance[quality_count].contact_phone = quality.contact_phone
            #         quality_assurance[quality_count].contact_email = quality.contact_email
            #         quality_assurance[quality_count].updated_by_id = data.updated_by_id

            #     else:
            #         quality_type = "Quality Assurance"
            #         new_quality = Site_Assess_Review(
            #             site_id = id,
            #             date = quality.date,
            #             salutation = quality.salutation,
            #             first_name = quality.first_name,
            #             last_name = quality.last_name,
            #             role = quality.role,
            #             contact_phone = quality.contact_phone,
            #             contact_email = quality.contact_email,
            #             review_type = quality_type,
            #             created_by_id = data.updated_by_id
            #         )
            #         db.add(new_quality)
            #     quality_count += 1

           

    def delete_reviewer(self,id):
        db = next(get_db())
        try:
            reviewer = db.query(Site_Assess_Review).filter(Site_Assess_Review.site_asmt_reviewer_id == id).first()
            if(reviewer):
                db.delete(reviewer)
                db.commit()
                return "Reviewer deleted Successfully"
            else:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="reviewer id doesn't exists")    
        finally:
            db.close()

