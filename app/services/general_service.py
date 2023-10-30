from app.model.general import General
from app.model.site import Site
from app.model.cr_gen_facilities_affiliations import GeneralAffiliations
from app.model.cr_gen_education import GeneralEducation
from app.model.cr import Cr
from app.model.contacts import Contacts
from app.model.institution import Institution
from app.model.country_details import CountryDetails
from app.model.site import Site
from app.model.cities import City
from app.model.cr_roles import Cr_Roles
from app.model.speciality import Speciality
from fastapi import HTTPException, status, FastAPI, UploadFile, File
import bcrypt
from fastapi.logger import logger
from app.db.database import get_db
from datetime import datetime
from app.model.miscellaneous import Miscellaneous
from sqlalchemy import func, desc,create_engine, Column, Integer, String, Date
from app.model.cr_status import Cr_Status
from app.model.speciality_subspeciality import SpecialitySubspeciality
from app.model.specialities_subspecialities import Specalitiess

from app.model.speciality import Speciality
from app.model.upload_documents import Upload_Documents
from app.model.document_status import Document_Status

# from fastapi import HTTPException, status,FastAPI, UploadFile, File
# from app.db.database import get_db 
from typing import List,Dict 
from typing import List,Dict 
# from sqlalchemy import func,desc,create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session 
import os
import pandas as pd
# from sqlalchemy import func,desc
# from app.model.department import Department
from datetime import datetime
from fastapi.responses import JSONResponse
from app.model.user import User

class General_Service:
    # def post_general(self, data):
    #     db = next(get_db())
    #     try:
    #         site = db.query(Site).filter(Site.site_name == data.company_site_name).first()
    #         site_id = site.site_id if site else None

    #         country = db.query(CountryDetails).filter(CountryDetails.country_name == data.country).first()
    #         country_id = country.country_id if country else None

    #         job_title = db.query(Cr_Roles).filter(Cr_Roles.cr_role == data.job_title).first()
    #         job_title_id = job_title.cr_role_id if job_title else None

    #         city = db.query(City).filter(City.city_name == data.city).first()
    #         city_id = city.city_id if city else None

    #         region = db.query(CountryDetails).filter(CountryDetails.region == data.region).first()
    #         region_id = region.country_id if region else None

    #         cr = db.query(Cr).filter(Cr.cr_code == data.cr_code, Cr.site_id == data.site_id).first()
    #         cr_id = cr.site_rec_cr_id if cr else None

            

    #         general = General(
    #             site_id=data.site_id,
    #             cr_code=cr_id,
    #             cr_name=data.cr_name,
    #             job_title=job_title_id,
    #             company_site_name=site_id,
    #             address_1=data.address_1,
    #             address_2=data.address_2,
    #             address_3=data.address_3,
    #             city=city_id,
    #             district=data.district,
    #             region=region_id,
    #             pincode=data.pincode,
    #             country=country_id,
    #             office_telephone=data.office_telephone,
    #             extension=data.extension,
    #             mobile_telephone=data.mobile_telephone,
    #             email=data.email,
    #             website=data.website,
    #             created_by_id=data.created_by_id,
    #             created=datetime.now()
    #         )
    #         db.add(general)
    #         db.flush()

    #         for education_data in data.education:
    #             education = GeneralEducation(
    #                 cr_general_id=general.cr_general_id,
    #                 degree_certificate=education_data.degree_certificate,
    #                 institution=education_data.institution,
    #                 speciality=education_data.speciality,
    #                 year_completed=education_data.year_completed,
    #                 created_by_id=general.created_by_id,
    #                 created=datetime.now()
    #             )
    #             db.add(education)

    #         for affiliation_data in data.affiliations:
    #             affiliation = GeneralAffiliations(
    #                 cr_general_id=general.cr_general_id,
    #                 primary_facility=affiliation_data.primary_facility,
    #                 facility_department_name=affiliation_data.facility_department_name,
    #                 address=affiliation_data.address,
    #                 created_by_id=general.created_by_id,
    #                 created=datetime.now()
    #             )
    #             db.add(affiliation)

    #         db.commit()
    #         return {"message": "General record created successfully."}

    #     except Exception as e:
    #         db.rollback()
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    #     finally:
    #         db.close()


    # def get_by_site_id(self, site_id):
    #     db = next(get_db())
    #     try:
    #         general = db.query(General).filter(General.site_id == site_id).first()
    #         if not general:
    #             return {"message": "No General record found for the provided site_id."}
    
    #         education = db.query(GeneralEducation).filter(GeneralEducation.cr_general_id == general.cr_general_id).all()
    #         affiliations = db.query(GeneralAffiliations).filter(GeneralAffiliations.cr_general_id == general.cr_general_id).all()
    
    #         general.education = education
    #         general.affiliations = affiliations
    
    #         site = db.query(Site).filter(Site.site_id == general.company_site_name).first()
    #         if site:
    #             general.company_site_name = site.site_name
    
    #         country = db.query(CountryDetails).filter(CountryDetails.country_id == general.country).first()
    #         if country:
    #             general.country = country.country_name
    
    #         job_title = db.query(Cr_Roles).filter(Cr_Roles.cr_role_id == general.job_title).first()
    #         if job_title:
    #             general.job_title = job_title.cr_role
    
    #         city = db.query(City).filter(City.city_id == general.city).first()
    #         if city:
    #             general.city = city.city_name
    
    #         region = db.query(CountryDetails).filter(CountryDetails.country_id == general.region).first()
    #         if region:
    #             general.region = region.region
    
    #         cr = db.query(Cr).filter(Cr.site_rec_cr_id == general.cr_code).first()
    #         if cr:
    #             general.cr_code = cr.cr_code


    #         return general
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #     finally:
    #         db.close()




    def get_cr_by_id(self, id):  
        db = next(get_db())
        try:
            cr = db.query(General).filter(General.cr_general_id == id).first()
            
            if cr:
                site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                salutation = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == cr.salutation).first()
                cr_experience = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == cr.cr_experience).first()
                good_clinical_practice = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == cr.certificate_of_good_clinical_practice).first()
                cv_available = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == cr.cv_available).first()
                cr_object = {
                    "cr_general_id":cr.cr_general_id,
                    "site_id":cr.site_id,
                    "site_code":site.site_code,
                    "cr_code":cr.cr_code,
                    "salutation":salutation.value,
                    "full_name":cr.full_name,
                    # "last_name":cr.last_name,
                    "speciality":cr.speciality,
                    "cr_experience": cr_experience.value,
                    "good_clinical_practice":good_clinical_practice.value,
                    "cv_available":cv_available.value,
                    "role":cr.role,
                    "cr_status":cr.cr_status,
                    "clinical_phases":cr.clinical_phases
                }

                education = db.query(GeneralEducation).filter(GeneralEducation.cr_general_id == id).all()
                facilities = db.query(GeneralAffiliations).filter(GeneralAffiliations.cr_general_id == id).all()
                cr_object['education'] = education
                cr_object['facilities'] = facilities
            return cr_object   

                
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()



    def put_general(self,cr_general_id, data):
        db = next(get_db())
        try:
            general = db.query(General).filter(General.cr_general_id == cr_general_id).first()
            salutation = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == data.salutation.lower()).first()
            cr_experience = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == data.cr_experience.lower()).first()
            good_clinical_practice = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == data.good_clinical_practice.lower()).first()
            cv_available = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == data.cv_available.lower()).first()
            if not general:
                existing_cr = db.query(General).filter(General.cr_code == data.cr_code).first()
                if(existing_cr):
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="CR Code already exists")  
                add_cr = General(
                    site_id=data.site_id,
                    cr_code=data.cr_code,
                    salutation = salutation.miscellaneous_id,
                    full_name=data.full_name,
                    # last_name=data.last_name,
                    speciality = data.speciality,
                    certificate_of_good_clinical_practice = good_clinical_practice.miscellaneous_id,
                    role = data.role,
                    cr_experience = cr_experience.miscellaneous_id,
                    cv_available = cv_available.miscellaneous_id,
                    cr_status = data.cr_status,
                    clinical_phases = data.clinical_phases,
                    created_by_id=data.created_by_id,
                    created=datetime.now()
                )
                db.add(add_cr)

                db.flush()

                for education_data in data.education:
                    education = GeneralEducation(
                        cr_general_id=add_cr.cr_general_id,
                        degree_certificate=education_data.degree_certificate,
                        institution=education_data.institution,
                        speciality=education_data.speciality,
                        year_completed=education_data.year_completed,
                        created_by_id=data.created_by_id,
                        created=datetime.now()
                    )
                    db.add(education)

                for affiliation_data in data.affiliations:
                    affiliation = GeneralAffiliations(
                        cr_general_id=add_cr.cr_general_id,
                        primary_facility=affiliation_data.primary_facility,
                        facility_department_name=affiliation_data.facility_department_name,
                        address=affiliation_data.address,
                        created_by_id=data.created_by_id,
                        created=datetime.now()
                    )
                    db.add(affiliation)

                db.commit()
                return {"message": "General record created successfully."}
            else:
                general.site_id=data.site_id
                general.cr_code=data.cr_code
                general.salutation = salutation.miscellaneous_id
                general.full_name=data.full_name
                # general.last_name=data.last_name
                general.speciality = data.speciality
                general.certificate_of_good_clinical_practice = good_clinical_practice.miscellaneous_id
                general.role = data.role
                general.cr_experience = cr_experience.miscellaneous_id
                general.cv_available = cv_available.miscellaneous_id
                general.cr_status = data.cr_status
                general.clinical_phases = data.clinical_phases
                general.updated_by_id=data.created_by_id
                general.updated=datetime.now()

                for education_data in data.education:
                    
                    education = db.query(GeneralEducation).filter(
                        GeneralEducation.cr_gen_edu_id == education_data.cr_gen_edu_id
                    ).first()
                    if education:
                        education.degree_certificate = education_data.degree_certificate
                        education.institution = education_data.institution
                        education.speciality = education_data.speciality
                        education.year_completed = education_data.year_completed
                        education.updated_by_id = data.created_by_id
                        education.updated = datetime.now()
                        db.add(education)
                    else:
                        education = GeneralEducation(
                            cr_general_id=general.cr_general_id,
                            degree_certificate=education_data.degree_certificate,
                            institution=education_data.institution,
                            speciality=education_data.speciality,
                            year_completed=education_data.year_completed,
                            created_by_id=data.created_by_id,
                            created=datetime.now()
                        )
                        db.add(education)    

                for affiliation_data in data.affiliations:
                    
                    affiliation = db.query(GeneralAffiliations).filter(
                        GeneralAffiliations.cr_gen_fac_aff_id == affiliation_data.cr_gen_fac_aff_id
                    ).first()
                    if affiliation:
                        affiliation.primary_facility = affiliation_data.primary_facility
                        affiliation.facility_department_name = affiliation_data.facility_department_name
                        affiliation.address = affiliation_data.address
                        affiliation.updated_by_id = data.created_by_id
                        affiliation.updated = datetime.now()
                    
                        db.add(affiliation)
                    else:
                        affiliation = GeneralAffiliations(
                            cr_general_id=general.cr_general_id,
                            primary_facility=affiliation_data.primary_facility,
                            facility_department_name=affiliation_data.facility_department_name,
                            address=affiliation_data.address,
                            created_by_id=data.created_by_id,
                            created=datetime.now()
                        )
                        db.add(affiliation)   

                db.commit()
                return {"message": "General record updated successfully."}
     
        finally:
            db.close()        



           
            # for education_data in data.education:
            #     if education_data.cr_gen_edu_id:
            #         education = db.query(GeneralEducation).filter(
            #             GeneralEducation.cr_gen_edu_id == education_data.cr_gen_edu_id
            #         ).first()
            #         if education:
            #             education.degree_certificate = education_data.degree_certificate
            #             education.institution = education_data.institution
            #             education.speciality = education_data.speciality
            #             education.year_completed = education_data.year_completed
            #             education.updated_by_id = data.updated_by_id
            #             education.updated = datetime.now()
            #     else:
            #         education = GeneralEducation(
            #             cr_general_id=general.cr_general_id,
            #             degree_certificate=education_data.degree_certificate,
            #             institution=education_data.institution,
            #             speciality=education_data.speciality,
            #             year_completed=education_data.year_completed,
            #             created_by_id=data.updated_by_id,
            #             created=datetime.now()
            #         )
            #         db.add(education)

            # for affiliation_data in data.affiliations:
            #     if affiliation_data.cr_gen_fac_aff_id:
            #         affiliation = db.query(GeneralAffiliations).filter(
            #             GeneralAffiliations.cr_gen_fac_aff_id == affiliation_data.cr_gen_fac_aff_id
            #         ).first()
            #         if affiliation:
            #             affiliation.primary_facility = affiliation_data.primary_facility
            #             affiliation.facility_department_name = affiliation_data.facility_department_name
            #             affiliation.address = affiliation_data.address
            #             affiliation.updated_by_id = data.updated_by_id
            #             affiliation.updated = datetime.now()
            #     else:
            #         affiliation = GeneralAffiliations(
            #             cr_general_id=general.cr_general_id,
            #             primary_facility=affiliation_data.primary_facility,
            #             facility_department_name=affiliation_data.facility_department_name,
            #             address=affiliation_data.address,
            #             created_by_id=data.updated_by_id,
            #             created=datetime.now()
            #         )
            #         db.add(affiliation)

            # db.commit()
            # return {"message": "General record updated successfully."}

        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        # finally:
        #     db.close()

    def get_crs(self,org_id):
        db = next(get_db())
        try:
            user_data = db.query(User).filter(User.org_id == org_id).all()
            cr_list = []
            if user_data:  
                for user in user_data:
                    CRs = db.query(General).filter(General.created_by_id == user.id).order_by(desc(General.created)).all()
                    for cr in CRs:
                        site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                        cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                        speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                        .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                        .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                        .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()

                        if(speciality):

                            cr_object = {
                                "cr_general_id":cr.cr_general_id,
                                "site_id":cr.site_id,
                                "site_code":site.site_code,
                                "cr_code":cr.cr_code,
                                "full_name":cr.full_name,
                                "speciality":speciality.speciality,
                                "sub_speciality":speciality.subspeciality,
                                "cr_status":cr_status.cr_status
                            }
                        else:
                            cr_object = {
                                "cr_general_id":cr.cr_general_id,
                                "site_id":cr.site_id,
                                "site_code":site.site_code,
                                "cr_code":cr.cr_code,
                                "full_name":cr.full_name,
                                "speciality":"",
                                "sub_speciality":"",
                                "cr_status":cr_status.cr_status
                            }

                        # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                        # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                        # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                        # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()    
                                
                        # yes_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                        # no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()

                        # yes_upload_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.document_attached == yes_document_attached.miscellaneous_id).all()
                        # no_upload_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()

                        # if yes_upload_documents:
                        #     # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                        #     # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                        #     # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                        #     # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        #     yes_documents_list = []
                        #     for document in yes_upload_documents:
                        #         yes_documents_list.append(document.status)

                        #     document_status = None  
                        #     if all(status is None or status == pending_verification.documentstatus_id for status in yes_documents_list):
                        #         document_status = "Pending"
                        #     elif all(status == approved_document.documentstatus_id for status in yes_documents_list):
                        #         document_status = "Completed"
                        #     elif all(status == rejected_document.documentstatus_id for status in yes_documents_list):
                        #         document_status = "Rejected"
                        #     elif pending_verification.documentstatus_id in yes_documents_list or approved_document.documentstatus_id in yes_documents_list or rejected_document.documentstatus_id in yes_documents_list:
                        #         document_status = "Pending"    

                        #     cr_object['document_status'] = document_status 
                        # elif no_upload_documents:

                        #     cr_object['document_status'] = "Pending"

                        # else:
                        #     cr_object['document_status'] = "Not Started"  

                        # cr_list.append(cr_object)
                        is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                        no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                        no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                        cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                        results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                        final_result = []
                        if(results):
                            document_dict = {}
                            for result in results:
                                document_name = result.document_name
                                if document_name not in document_dict:
                                    document_dict[document_name] = {
                                        "site_id": result.site_id,
                                        "cr_id": result.cr_code,
                                        "screen_label_name": result.screen_label_name,
                                        "document_name": document_name,
                                        "document_attached": result.document_attached,
                                        # "status": result.status,
                                        "remarks": result.remarks,
                                        "versions": []
                                    }
                                document_dict[document_name]["versions"].append({
                                    "upload_document_id": result.upload_document_id,
                                    "version": result.version,
                                    "attachment": result.attachment,
                                    "status": result.status,
                                    "created": result.created
                                })

                            # Convert the dictionary values to a list
                            grouped_results = list(document_dict.values())


                            latest_version_dict = {}

                # Iterate through the grouped_results and update the latest version
                            for item in grouped_results:
                                document_name = item["document_name"]
                                version_list = item["versions"]
                                
                                # Sort the version list by created timestamp in descending order
                                version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                                # Get the latest version
                                latest_version = version_list[0]["version"]
                                
                                # Update the latest version in the dictionary
                                latest_version_dict[document_name] = latest_version

                            # Create a list of objects with the latest version and created timestamp
                            # final_result = []

                            for item in grouped_results:
                                document_name = item["document_name"]
                                
                                # Check if the document_name is in the latest_version_dict
                                if document_name in latest_version_dict:
                                    latest_version = latest_version_dict[document_name]
                                    
                                    # Find the version with the latest version
                                    for version in item["versions"]:
                                        if version["version"] == latest_version:
                                            # Create a new object with the required fields
                                            latest_version_item = {
                                                "site_id": item["site_id"],
                                                "cr_id": item["cr_id"],
                                                "screen_label_name": item["screen_label_name"],
                                                "document_name": item["document_name"],
                                                "document_attached": item["document_attached"],
                                                "remarks": item["remarks"],
                                                "upload_document_id": version["upload_document_id"],
                                                "version": version["version"],
                                                "status": version["status"],
                                                "created": version["created"]
                                            }
                                            final_result.append(latest_version_item)


                        # return cr_documents
                        if final_result:

                            org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                            users = db.query(User).filter(User.org_id == org_id.org_id).all()
                            pending_document_list = []
                            for user in users:
                                pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                                if(pending_status):
                                    pending_document_list.extend(pending_status)
                            pending_document_obj = None        
                            for document in pending_document_list:
                                if document.document_status_description.lower() == "pending document":
                                    pending_document_obj = document
                                    break 
                            
                            pending_verification_list = []
                            for user in users:
                                verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                                if(verification_status):
                                    pending_verification_list.extend(verification_status)
                            pending_verification_obj = None        
                            for document in pending_verification_list:
                                if document.document_status_description.lower() == "pending verification":
                                    pending_verification_obj = document
                                    break 

                            approved_document_list = []
                            for user in users:
                                approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                                if(approved_status):
                                    approved_document_list.extend(approved_status)
                            approved_document_obj = None        
                            for document in approved_document_list:
                                if document.document_status_description.lower() == "approved":
                                    approved_document_obj = document
                                    break      

                            rejected_document_list = []
                            for user in users:
                                rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                                if(rejected_status):
                                    rejected_document_list.extend(rejected_status)
                            rejected_document_obj = None        
                            for document in rejected_document_list:
                                if document.document_status_description.lower() == "rejected":
                                    rejected_document_obj = document
                                    break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                            documents_list = []
                            for document in final_result:
                                documents_list.append(document['status'])

                            document_status = None 
                            if(pending_verification_obj and approved_document_obj and rejected_document_obj):
                                if all(status is None or status == pending_verification_obj.documentstatus_id for status in documents_list):
                                    document_status = "Pending"
                                elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                    document_status = "Completed"
                                elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                    document_status = "Rejected"
                                elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                    document_status = "Pending"  
                                cr_object['document_status'] = document_status
                            else:
                                cr_object['document_status'] = "Not Started"       
                        elif no_cr_documents:

                            cr_object['document_status'] = "Pending"

                        else:
                            cr_object['document_status'] = "Not Started"  

                        cr_list.append(cr_object)       

            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Org id has no cr's.")
            return cr_list
        finally:
            db.close()    

    def delete_gen_edu(self, cr_gen_edu_id):
        db = next(get_db())
        try:
            education_id = db.query(GeneralEducation).filter(GeneralEducation.cr_gen_edu_id == cr_gen_edu_id).first()
            if(education_id):
                db.delete(education_id)
                db.commit()
                return{"successs":"General Education record deleted sucessfully"}
            else:
                return{"error":" No record found with that cr_gen_edu_id"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def delete_gen_fac(self, cr_gen_fac_aff_id):
        db = next(get_db())
        try:
            facility_id = db.query(GeneralAffiliations).filter(GeneralAffiliations.cr_gen_fac_aff_id == cr_gen_fac_aff_id).first()
            if(facility_id):
                db.delete(facility_id)
                db.commit()
                return{"successs":"General Facility record deleted sucessfully"}
            else:
                return{"error":" No record found with that cr_gen_fac_aff_id"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_by_site_id_and_site_rec_cr_id(self, site_id, site_rec_cr_id):
        db = next(get_db())
        try:
            general = db.query(General).filter(General.site_id == site_id, General.cr_code == site_rec_cr_id).first()
            if not general:
                return {"message": "No General record found for the provided site_id and site_rec_cr_id."}
    
            education = db.query(GeneralEducation).filter(GeneralEducation.cr_general_id == general.cr_general_id).all()
            affiliations = db.query(GeneralAffiliations).filter(GeneralAffiliations.cr_general_id == general.cr_general_id).all()
    
            general.education = education
            general.affiliations = affiliations
    
            site = db.query(Site).filter(Site.site_id == general.company_site_name).first()
            if site:
                general.company_site_name = site.site_name
    
            country = db.query(CountryDetails).filter(CountryDetails.country_id == general.country).first()
            if country:
                general.country = country.country_name
    
            job_title = db.query(Cr_Roles).filter(Cr_Roles.cr_role_id == general.job_title).first()
            if job_title:
                general.job_title = job_title.cr_role
    
            city = db.query(City).filter(City.city_id == general.city).first()
            if city:
                general.city = city.city_name
    
            region = db.query(CountryDetails).filter(CountryDetails.country_id == general.region).first()
            if region:
                general.region = region.region
    
            cr = db.query(Cr).filter(Cr.site_rec_cr_id == general.cr_code).first()
            if cr:
                general.cr_code = cr.cr_code
    
            return general
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def get_site_crs(self,id):
        db = next(get_db())
        try:
            crs = db.query(General).filter(General.site_id == id).all()
            return crs  

        finally:
            db.close()   

    def filter_cr(self,data):
        db = next(get_db())
        try:
            if(data.site_id > 0 and data.cr_id > 0 and data.cr_status > 0 and data.speciality_id > 0):
                CRs = db.query(General).filter(General.site_id == data.site_id, General.cr_general_id == data.cr_id, General.cr_status == data.cr_status, General.speciality == data.speciality_id).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }
                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"       
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list

            elif(data.site_id > 0 and data.cr_id > 0 and data.cr_status > 0 and data.speciality_id == 0):
                CRs = db.query(General).filter(General.site_id == data.site_id, General.cr_general_id == data.cr_id, General.cr_status == data.cr_status).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"   
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list

            elif(data.site_id > 0 and data.cr_id > 0 and data.speciality_id > 0 and data.cr_status == 0):
                CRs = db.query(General).filter(General.site_id == data.site_id, General.cr_general_id == data.cr_id, General.speciality == data.speciality_id).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"   
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list                  

            elif(data.site_id > 0 and data.speciality_id > 0 and data.cr_status > 0 and data.cr_id == 0):
                CRs = db.query(General).filter(General.site_id == data.site_id, General.speciality == data.speciality_id, General.cr_status == data.cr_status).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }
                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"   
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list   

            elif(data.cr_id > 0 and data.speciality_id > 0 and data.cr_status > 0 and data.site_id == 0):
                CRs = db.query(General).filter(General.cr_general_id == data.cr_id, General.speciality == data.speciality_id, General.cr_status == data.cr_status).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }
                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started" 
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list                  
                   
            
            elif(data.site_id > 0 and data.cr_id > 0 and data.speciality_id == 0 and data.cr_status == 0):
                CRs = db.query(General).filter(General.site_id == data.site_id, General.cr_general_id == data.cr_id).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }
                    

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"   
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       
                return cr_list                  

            elif(data.site_id == 0 and data.cr_id == 0 and data.speciality_id > 0 and data.cr_status > 0):
                CRs = db.query(General).filter(General.speciality == data.speciality_id, General.cr_status == data.cr_status).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"  
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list  

            elif(data.site_id > 0 and data.cr_id == 0 and data.speciality_id == 0 and data.cr_status > 0):
                CRs = db.query(General).filter(General.site_id == data.site_id, General.cr_status == data.cr_status).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started" 
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list                  
            
            elif(data.site_id > 0 and data.cr_id == 0 and data.speciality_id > 0 and data.cr_status == 0):
                CRs = db.query(General).filter(General.site_id == data.site_id, General.speciality == data.speciality_id).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"  
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list 
            
            elif(data.site_id == 0 and data.cr_id > 0 and data.speciality_id > 0 and data.cr_status == 0):
                CRs = db.query(General).filter(General.cr_general_id == data.cr_id, General.speciality == data.speciality_id).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"   
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list 

            elif(data.site_id == 0 and data.cr_id > 0 and data.speciality_id == 0 and data.cr_status > 0):
                CRs = db.query(General).filter(General.cr_general_id == data.cr_id, General.cr_status == data.cr_status).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"   
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list 
    

            elif(data.site_id > 0 and data.cr_id == 0 and data.speciality_id == 0 and data.cr_status == 0):
                CRs = db.query(General).filter(General.site_id == data.site_id).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"  
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list                  

            elif(data.site_id == 0 and data.cr_id == 0 and data.speciality_id == 0 and data.cr_status > 0):
                CRs = db.query(General).filter(General.cr_status == data.cr_status).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"   
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list                  
            
            elif(data.site_id == 0 and data.cr_id == 0 and data.speciality_id > 0 and data.cr_status == 0):
                CRs = db.query(General).filter(General.speciality == data.speciality_id).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started"
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list 

            elif(data.site_id == 0 and data.cr_id > 0 and data.speciality_id == 0 and data.cr_status == 0):
                CRs = db.query(General).filter(General.cr_general_id == data.cr_id).order_by(desc(General.created)).all()
                cr_list = []
                for cr in CRs:
                    site = db.query(Site).filter(Site.site_id == cr.site_id).first()
                    cr_status = db.query(Cr_Status).filter(Cr_Status.cr_status_id == cr.cr_status).first()
                    speciality = db.query(Speciality.speciality,SpecialitySubspeciality.subspeciality,Specalitiess.specialities_subspecialities_id)\
                    .join(Speciality,SpecialitySubspeciality.speciality_id == Speciality.id )\
                    .join(Specalitiess,Specalitiess.spec_sub_id == SpecialitySubspeciality.id)\
                    .filter(Specalitiess.specialities_subspecialities_id == cr.speciality).first()    
                    
                    if(speciality):

                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":speciality.speciality,
                            "sub_speciality":speciality.subspeciality,
                            "cr_status":cr_status.cr_status
                        }
                    else:
                        cr_object = {
                            "cr_general_id":cr.cr_general_id,
                            "site_id":cr.site_id,
                            "site_code":site.site_code,
                            "cr_code":cr.cr_code,
                            "full_name":cr.full_name,
                            "speciality":"",
                            "sub_speciality":"",
                            "cr_status":cr_status.cr_status
                        }

                    is_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "yes").first()
                    no_document_attached = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == "no").first()
                    no_cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == no_document_attached.miscellaneous_id).all()
                    cr_documents = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id,Upload_Documents.document_attached == is_document_attached.miscellaneous_id).all()

                    results = db.query(Upload_Documents).filter(Upload_Documents.cr_code == cr.cr_general_id, Upload_Documents.screen_type_name == "Clinical Researcher", Upload_Documents.document_attached == is_document_attached.miscellaneous_id).order_by(desc(Upload_Documents.created)).all()

                        # Create a dictionary to group documents by document_name
                    final_result = []
                    if(results):
                        document_dict = {}
                        for result in results:
                            document_name = result.document_name
                            if document_name not in document_dict:
                                document_dict[document_name] = {
                                    "site_id": result.site_id,
                                    "cr_id": result.cr_code,
                                    "screen_label_name": result.screen_label_name,
                                    "document_name": document_name,
                                    "document_attached": result.document_attached,
                                    "remarks": result.remarks,
                                    "versions": []
                                }
                            document_dict[document_name]["versions"].append({
                                "upload_document_id": result.upload_document_id,
                                "version": result.version,
                                "attachment": result.attachment,
                                "status": result.status,
                                "created": result.created
                            })

                        grouped_results = list(document_dict.values())

                        latest_version_dict = {}

                        for item in grouped_results:
                            document_name = item["document_name"]
                            version_list = item["versions"]
                                
                            version_list.sort(key=lambda x: x["created"], reverse=True)
                                
                            latest_version = version_list[0]["version"]
                                
                            latest_version_dict[document_name] = latest_version

                        for item in grouped_results:
                            document_name = item["document_name"]
                                
                            if document_name in latest_version_dict:
                                latest_version = latest_version_dict[document_name]
                                    
                                for version in item["versions"]:
                                    if version["version"] == latest_version:
                                        latest_version_item = {
                                            "site_id": item["site_id"],
                                            "cr_id": item["cr_id"],
                                            "screen_label_name": item["screen_label_name"],
                                            "document_name": item["document_name"],
                                            "document_attached": item["document_attached"],
                                            "remarks": item["remarks"],
                                            "upload_document_id": version["upload_document_id"],
                                            "version": version["version"],
                                            "status": version["status"],
                                            "created": version["created"]
                                        }
                                        final_result.append(latest_version_item)

                    if final_result:
                        org_id = db.query(User).filter(User.id == cr.created_by_id).first()
                        users = db.query(User).filter(User.org_id == org_id.org_id).all()
                        pending_document_list = []
                        for user in users:
                            pending_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(pending_status):
                                pending_document_list.extend(pending_status)
                        pending_document_obj = None        
                        for document in pending_document_list:
                            if document.document_status_description.lower() == "pending document":
                                pending_document_obj = document
                                break 
                            
                        pending_verification_list = []
                        for user in users:
                            verification_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(verification_status):
                                pending_verification_list.extend(verification_status)
                        pending_verification_obj = None        
                        for document in pending_verification_list:
                            if document.document_status_description.lower() == "pending verification":
                                pending_verification_obj = document
                                break 

                        approved_document_list = []
                        for user in users:
                            approved_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(approved_status):
                                approved_document_list.extend(approved_status)
                        approved_document_obj = None        
                        for document in approved_document_list:
                            if document.document_status_description.lower() == "approved":
                                approved_document_obj = document
                                break      

                        rejected_document_list = []
                        for user in users:
                            rejected_status = db.query(Document_Status).filter(Document_Status.created_by_id == user.id).all()
                            if(rejected_status):
                                rejected_document_list.extend(rejected_status)
                        rejected_document_obj = None        
                        for document in rejected_document_list:
                            if document.document_status_description.lower() == "rejected":
                                rejected_document_obj = document
                                break
                            # pending_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending document").first()
                            # pending_verification = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "pending verification").first()
                            # approved_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "approved").first()
                            # rejected_document = db.query(Document_Status).filter(func.lower(Document_Status.document_status_description) == "rejected").first()
                        documents_list = []
                        for document in final_result:
                            documents_list.append(document['status'])

                        document_status = None 
                        if(approved_document_obj and pending_verification_obj and rejected_document_obj):
                            if all(status is None or status == pending_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Pending"
                            elif all(status == approved_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Completed"
                            elif all(status == rejected_document_obj.documentstatus_id for status in documents_list):
                                document_status = "Rejected"
                            elif pending_verification_obj.documentstatus_id in documents_list or approved_document_obj.documentstatus_id in documents_list or rejected_document_obj.documentstatus_id in documents_list:
                                document_status = "Pending" 
                            cr_object['document_status'] = document_status
                        else:
                            cr_object['document_status'] = "Not Started" 
                    elif no_cr_documents:

                        cr_object['document_status'] = "Pending"

                    else:
                        cr_object['document_status'] = "Not Started"  

                    cr_list.append(cr_object)       

                return cr_list 
    
        finally:
            db.close()    

    def multiple_cr_upload(self, file_path: str,id,site_id):
        db = next(get_db())
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                # print("Csv Data:")
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
                # print("Excel Data:")
                # print(df)
            elif file_path.endswith('.xls'):
                df = pd.read_excel(file_path)  
                # print("Excel Data:")
                # print(df)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file format") 
            if df.empty:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
                        
            error_messages = []
            new_cr_added = False 
            cr_list = []
            for index, row in df.iterrows():
                cr_details = {
                    # "site_code": row["site_code"],
                    # "cr_code": row["cr_code"],
                    "salutation": row["salutation"],
                    "full_name" : row["full_name"],
                    "cr_experience" : row["cr_experience"],
                    "certificate_of_good_clinical_practice" : row["certificate_of_good_clinical_practice"],
                    # "cr_role_id" : row["cr_role_id"],
                    "cv_available": row["cv_available"]
                }

                latest_cr_subquery = db.query(General.cr_code).order_by(desc(func.cast(func.substr(General.cr_code, 4), Integer))).limit(1).subquery()

                latest_cr = db.query(General).filter(General.cr_code == latest_cr_subquery)

                latest_cr_result = latest_cr.first()

                latest_cr_code = latest_cr_result.cr_code

                # Extract the numeric part of the CR code and increment it
                current_number = int(latest_cr_code.split('-')[1])
                latest_added_cr = db.query(General).order_by(desc(General.cr_general_id)).first()
                new_number = latest_added_cr.cr_general_id + 1

                # Construct the new CR code with the incremented number
                new_cr_code = f"CR-{new_number}"
                
                
                
                                
                existing_cr = db.query(General).filter(
                    func.lower(General.cr_code) == new_cr_code.lower()
                ).first()
                if existing_cr:
                    error_messages.append(f"CR code '{cr_details['cr_code']}' already exists for {existing_cr.full_name}.")                   
                    # error_messages.append(f"Employee code '{emp_details['employee_code']}' already exists.")
                    
                else:
                    # Create a new employee record
                    # site_id = db.query(Site).filter(func.lower(Site.site_code) == cr_details["site_code"].lower()).first()
                    salutation = db.query(Miscellaneous).filter(func.lower(Miscellaneous.type) == "salutation", func.lower(Miscellaneous.value) == cr_details["salutation"].lower()).first()
                    cr_experience = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == cr_details["cr_experience"].lower()).first()
                    certificate_of_good_clinical_practice = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == cr_details["certificate_of_good_clinical_practice"].lower()).first()
                    # role = db.query(Cr_Roles).filter(Cr_Roles.cr_id == str(cr_details["cr_role_id"])).first()
                    cv_available = db.query(Miscellaneous).filter(func.lower(Miscellaneous.value) == cr_details["cv_available"].lower()).first()
                    cr_status = db.query(Cr_Status).filter(func.lower(Cr_Status.cr_status) == "created").first()
                    new_cr = General(
                        site_id= site_id,
                        cr_code= new_cr_code,
                        salutation=salutation.miscellaneous_id,
                        full_name=cr_details["full_name"],
                        cr_experience=cr_experience.miscellaneous_id,
                        certificate_of_good_clinical_practice = certificate_of_good_clinical_practice.miscellaneous_id,
                        # role = role.cr_role_id,
                        cv_available = cv_available.miscellaneous_id,
                        cr_status = cr_status.cr_status_id, 
                        created_by_id=id,
                        created=datetime.now()
                    )
                   
                    db.add(new_cr)
                    db.commit()
                    db.refresh(new_cr)
                    new_cr_added = True
           

            if new_cr_added:
                return {"message": "Data uploaded and processed successfully, new cr's added."}
            else:
                raise HTTPException(status_code=400, detail="No new cr's were added.")
                return {"message": "No new cr's were added."}
            
            if error_messages:
                response_content = {"error_messages": error_messages}
                return JSONResponse(content=response_content, status_code=400)
                return {"error_messages": error_messages}
        except HTTPException as e:
            raise e  
        except Exception as e:
            db.rollback()
            error_message = "Please once check the CR data :" + str(e)
            raise HTTPException(status_code=422, detail=error_message)
        finally:
            db.close()

    def get_all_crs(self):
        db = next(get_db())
        try:
            crs = db.query(General).order_by(desc(General.cr_general_id)).all()
            return crs
        finally:
            db.close()
