from app.db.database import get_db
from app.model.site_services import SiteServices
from app.model.service_category import Service_Category
from fastapi import HTTPException, status
from sqlalchemy import func,desc
from app.model.miscellaneous import Miscellaneous
from app.model.user import User

class Site_Services:
    def add_site_services(self, site_service_details):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == site_service_details.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_service_list = []
        for user in users:
            site_services = db.query(SiteServices).filter(SiteServices.created_by_id == user.id).all()
            if(site_services):
                existing_service_list.extend(site_services)
        check_existing_service = False
        if any(existing_service.site_service_id.lower() == site_service_details.site_service_id.lower() for existing_service in existing_service_list):
            check_existing_service = True
        # site_service = db.query(SiteServices).filter(func.lower(SiteServices.site_service_id) == site_service_details.site_service_id.lower()).first()
        if check_existing_service:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Site service id already exist.")
        else:
            try:
                new_site_service = SiteServices(
                    site_service_id  = site_service_details.site_service_id,
                    service_category = site_service_details.service_category,
                    service_category_description = site_service_details.service_category_description,
                    created_by_id = site_service_details.created_by_id
                )
                db.add(new_site_service)
                db.commit()
                db.refresh(new_site_service)
                return {"success" : "Site service added successfully"}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            finally:
                db.close()
    def site_services_list(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()       
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    all_services_list =[]
                    for user in list_of_users_related_to_org:
                        site_services = db.query(SiteServices.site_ser_id,SiteServices.service_category,SiteServices.site_service_id,SiteServices.service_category_description,Service_Category.service_category_id,Service_Category.service_category,Service_Category.description, Miscellaneous.value).join(Service_Category,Service_Category.service_category_id == SiteServices.service_category).join(Miscellaneous,Miscellaneous.miscellaneous_id == Service_Category.service_category_indicator).filter(SiteServices.created_by_id == user.id).order_by(desc(SiteServices.created)).all()
                        all_services_list.extend(site_services)
                    return {"site_services_list": all_services_list}
                else:
                    return {"response":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"response":f"user_id = {user_id} not found"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            # site_services = db.query(SiteServices.site_ser_id,SiteServices.service_category,SiteServices.site_service_id,SiteServices.service_category_description,Service_Category.service_category_id,Service_Category.service_category,Service_Category.description, Miscellaneous.value).join(Service_Category,Service_Category.service_category_id == SiteServices.service_category).join(Miscellaneous,Miscellaneous.miscellaneous_id == Service_Category.service_category_indicator).order_by(desc(SiteServices.created)).all()
            # return {"site_services_list": site_services}
        finally:
            db.close()

    def update_site_service(self,id,data):
        db = next(get_db())
        siteservice = db.query(SiteServices).filter(SiteServices.site_ser_id == id).first()
        try:
            if(siteservice):
                siteservice.service_category=data.service_category,
                siteservice.service_category_description=data.service_category_description,
                siteservice.updated_by_id=data.updated_by_id
                db.commit()
                return{"response":"Site Service Updated Successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Site Service not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
    
    def get_site_services(self,id):
        db = next(get_db())
        try:
            site_services = db.query(SiteServices).filter(SiteServices.site_ser_id == id).first()
            return {"site_services_list": site_services}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()     

    def filter_site_services(self,id):
        db = next(get_db())
        try:
            site_services = db.query(SiteServices).filter(SiteServices.service_category == id).all()
            return {"filtered_list": site_services}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close() 
