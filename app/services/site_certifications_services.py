from app.model.site_certifications import Site_Certifications
from app.db.database import get_db
from fastapi import HTTPException,status
from app.model.site_services import SiteServices
from sqlalchemy import func,desc,asc
from app.model.user import User

class Site_Certificatess:
    def Site_Certifications(self,data):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_certificate_list = []
        for user in users:
            certifications = db.query(Site_Certifications).filter(Site_Certifications.created_by_id == user.id).all()
            if(certifications):
                existing_certificate_list.extend(certifications)
        check_existing_certificate = False
        if any(existing_certificate.certification_id.lower() == data.certification_id.lower() for existing_certificate in existing_certificate_list):
            check_existing_certificate = True

        # site_certficate = db.query(Site_Certifications).filter(func.lower(Site_Certifications.certification_id) == data.certification_id.lower()).first()
        if check_existing_certificate:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Site Certification already exist.")
        else:
            try:
                new_sitecertificate = Site_Certifications(
                    certification_id=data.certification_id,
                    service_category_description=data.service_category_description,
                    certification_description=data.certification_description,
                    created_by_id=data.created_by_id
                )
                db.add(new_sitecertificate)
                db.commit()
                return{"Site Certifications are created Successfully"}
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create Site Certifications.")
            finally:
                db.close()

    def get_site_certifications_all(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    site_certs_list =[]
                    for user in list_of_users_related_to_org:
                        site_certs = db.query(Site_Certifications.certification_id,Site_Certifications.service_category_description,Site_Certifications.site_certification_id,Site_Certifications.certification_description,SiteServices.site_ser_id,SiteServices.service_category_description,SiteServices.site_service_id).join(SiteServices, Site_Certifications.service_category_description == SiteServices.site_ser_id).filter(Site_Certifications.created_by_id == user.id).order_by((Site_Certifications.created)).all()
            
                        site_certs_list.extend(site_certs)
                    return site_certs_list
                else:
                    return {"response":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"response":f"user_id = {user_id} not found"} 

            # site_certs = db.query(Site_Certifications.certification_id,Site_Certifications.service_category_description,Site_Certifications.site_certification_id,Site_Certifications.certification_description,SiteServices.site_ser_id,SiteServices.service_category_description,SiteServices.site_service_id).join(SiteServices, Site_Certifications.service_category_description == SiteServices.site_ser_id).order_by((Site_Certifications.created)).all()
            # return site_certs
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    def get_site_certifications_by_id(self,id):
        db = next(get_db())
        try:
            sitecertifications = db.query(Site_Certifications).filter(Site_Certifications.site_certification_id == id).all()
            return sitecertifications
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def update_site_certifications(self,id,data):
        db = next(get_db())
        updatecertifications = db.query(Site_Certifications).filter(Site_Certifications.site_certification_id == id).first()
        try:
            if(updatecertifications):
                updatecertifications.service_category_description=data.service_category_description,
                updatecertifications.certification_description=data.certification_description,
                updatecertifications.updated_by_id=data.updated_by_id
                db.commit()
                return{"response":"Site Certifications updated successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Site Certifications not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()       