from  app.model.services import Site_Services
from  app.model.site_services import SiteServices
from  app.model.service_category import Service_Category
from  app.model.site import Site
from fastapi import HTTPException,status
from app.db.database import get_db 
from sqlalchemy import desc,cast,String,Integer
from  app.model.miscellaneous import Miscellaneous


class  Service:
    # def add_service(self, data):
    #     db = next(get_db())
    #     try:
    #         if data.services_list :
    #             for service in data.services_list:
    #                 servicess_lists = [int(num) for num in service.split(",")]
    #                 for services in servicess_lists:
    #                     # print(services)
    #                     services_category = db.query(SiteServices.site_ser_id,SiteServices.site_service_id,SiteServices.service_category,SiteServices.service_category_description,
    #                     Service_Category.service_category_id,Service_Category.service_category,Service_Category.description)\
    #                     .join(Service_Category,Service_Category.service_category_id == data.service_category)\
    #                     .filter(SiteServices.site_ser_id == services).first()
    #                     # print(services_category)
    #                     add_serv = db.query(Site_Services)\
    #                     .filter(Site_Services.services == services_category.service_category_description)\
    #                     .filter(Site_Services.site_id == data.site_id).all()
    #                     print(add_serv)
    #                     if services_category:
    #                         if add_serv:
    #                             raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="services id already exists")
    #                         else:
    #                             print(services_category)
    #                             print(data.site_id)
    #                             new_service = Site_Services(
    #                                 site_id=data.site_id,
    #                                 services=int(services_category.site_ser_id),
    #                                 service_category=int(services_category.service_category_id),
    #                                 remarks=data.remarks,
    #                                 created_by_id=data.created_by_id
    #                             )
    #                             db.add(new_service)
    #                             db.commit()
    #                             db.refresh(new_service)
    #             return {"services": "services added successfully"}
    #         else:
    #             raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="services name is empty.")
    #     finally:        
    #         db.close()
    # def add_service(self, data):
    #     db = next(get_db())
    #     try:
    #         if data.services_list:
    #             for service in data.services_list:
    #                 servicess_lists = [int(num) for num in service.split(",")]
    #                 for services in servicess_lists:
    #                     services_category = db.query(SiteServices.site_ser_id, SiteServices.site_service_id, SiteServices.service_category, SiteServices.service_category_description,
    #                     Service_Category.service_category_id, Service_Category.service_category, Service_Category.description)\
    #                     .join(Service_Category, Service_Category.service_category_id == data.service_category)\
    #                     .filter(SiteServices.site_ser_id == services).first()

    #                     if services_category:
    #                         add_serv = db.query(Site_Services)\
    #                         .filter(Site_Services.services == services)\
    #                         .filter(Site_Services.site_id == data.site_id).all()

    #                         if add_serv:
    #                             raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Service id already exists")
    #                         else:
    #                             new_service = Site_Services(
    #                                 site_id=data.site_id,
    #                                 services=int(services_category.site_ser_id),
    #                                 service_category=int(services_category.service_category_id),
    #                                 remarks=data.remarks,
    #                                 created_by_id=data.created_by_id
    #                             )
    #                             db.add(new_service)
    #                             db.commit()
    #                             db.refresh(new_service)
    #                     else:
    #                         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Service not found for ID {services}")
    #         return {"services": "Services added successfully"}
    #     except HTTPException as http_exc:
    #         raise http_exc  # Re-raise the HTTP exception
    #     except Exception as e:
    #         logging.error(f"Error while adding services: {str(e)}")
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="services name is empty.")
    #     finally:
    #         db.close()
    def add_service(self, data):
        db = next(get_db())
        try:
            if data.services_list:
                for service in data.services_list:
                    servicess_lists = [int(num) for num in service.split(",")]
                    for services in servicess_lists:
                        if isinstance(services, int):
                            # Handle the case where 'services' is an integer
                            services_category = db.query(SiteServices.site_ser_id, SiteServices.site_service_id, SiteServices.service_category, SiteServices.service_category_description,
                            Service_Category.service_category_id, Service_Category.service_category, Service_Category.description)\
                            .join(Service_Category, Service_Category.service_category_id == data.service_category)\
                            .filter(SiteServices.site_ser_id == services).first()
                        elif isinstance(services, dict):
                            # Handle the case where 'services' is a dictionary
                            service_id = services.get("service_id")
                            services_category = db.query(SiteServices.site_ser_id, SiteServices.site_service_id, SiteServices.service_category, SiteServices.service_category_description,
                            Service_Category.service_category_id, Service_Category.service_category, Service_Category.description)\
                            .join(Service_Category, Service_Category.service_category_id == data.service_category)\
                            .filter(SiteServices.site_ser_id == service_id).first()
                        else:
                            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid 'services' data structure")

                        if services_category:
                            add_serv = db.query(Site_Services)\
                            .filter(Site_Services.services == services)\
                            .filter(Site_Services.site_id == data.site_id).all()

                            if add_serv:
                                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Service id already exists")
                            else:
                                new_service = Site_Services(
                                    site_id=data.site_id,
                                    services=int(services_category.site_ser_id),
                                    service_category=int(services_category.service_category_id),
                                    remarks=data.remarks,
                                    created_by_id=data.created_by_id
                                )
                                db.add(new_service)
                                db.commit()
                                db.refresh(new_service)
                        else:
                            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Service not found for ID {services}")
            return {"services": "Services added successfully"}
        # except HTTPException as http_exc:
        #     raise http_exc  # Re-raise the HTTP exception
        # except Exception as e:
        #     logging.error(f"Error while adding services: {str(e)}")
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while adding services.")
        finally:
            db.close()



    # def  Site_Services(self,data):
    #     db =  next(get_db())
    #     unique_service = db.query(Site_Services).filter(Site_Services.site_id == data.site_id).filter(Site_Services.services == data.services).first()
    #     if(unique_service):
    #         return{"response":"Service already added for this Site"}
    #     else:    
    #         try:
    #             new_user = Site_Services(
    #                 site_id=data.site_id,
    #                 service_category = data.service_category,
    #                 services = data.services,
    #                 short_name=data.short_name,
    #                 remarks=data.remarks,
    #                 created_by_id=data.created_by_id
    #             )

    #             db.add(new_user)
    #             db.commit()
    #             db.refresh(new_user)
    #             return {"message":"service created"}
    #         except Exception as e:
    #             db.rollback()
    #             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    #         finally:
    #             db.close()

    def get_site_service_all(self):
        db = next(get_db())
        try:
            site_sercs = db.query(Site_Services.service_id,Site_Services.site_id,Site_Services.remarks,Site_Services.service_category,Site_Services.services,Site.site_code,Site.site_name,SiteServices.site_ser_id,SiteServices.site_service_id,SiteServices.service_category_description,Service_Category.service_category_id,Service_Category.description,Service_Category.service_category,Site_Services.services,Miscellaneous.value)\
            .join(Site,Site.site_id == Site_Services.site_id)\
            .join(SiteServices,SiteServices.site_ser_id == cast(Site_Services.services, Integer))\
            .join(Service_Category,Service_Category.service_category_id == cast(Site_Services.service_category,Integer))\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Service_Category.service_category_indicator)\
            .order_by(desc(Site_Services.created)).all()
            return site_sercs
        except ValueError as e:
            error_message = f"An error occurred while casting 'services' column: {str(e)}"
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
    
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
                # raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    # def get_site_service_by_id(self,id):
    #     db = next(get_db())
    #     try:
    #         site_sercs = db.query(Site_Services.service_id,Site_Services.site_id,Site_Services.remarks,Site_Services.short_name,Service_Category.service_category_id,Service_Category.description,Service_Category.service_category,SiteServices.site_ser_id,SiteServices.site_service_id,SiteServices.service_category_description)\
    #         .join(Service_Category, Site_Services.service_category == Service_Category.service_category_id)\
    #         .join(SiteServices, SiteServices.site_ser_id == Site_Services.services)\
    #         .filter(Site_Services.service_id == id).first()
    #         return site_sercs
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    #     finally:
    #         db.close()
    def get_site_service_by_id(self, id):
        db = next(get_db())
        try:
            site_service = db.query(
                Site_Services.service_id,
                Site_Services.site_id,
                Site_Services.remarks,
                Service_Category.service_category_id,
                Service_Category.description,
                Service_Category.service_category,
                SiteServices.site_ser_id,
                SiteServices.site_service_id,
                SiteServices.service_category_description
            ).join(Service_Category,Service_Category.service_category_id == cast(Site_Services.service_category,Integer))\
            .join(SiteServices,SiteServices.site_ser_id == cast(Site_Services.services, Integer)).filter(Site_Services.service_id == id).first()
            return site_service
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

 
    def update_site_service_by_id(self, id, data):
        db = next(get_db())
        siteservices = db.query(Site_Services).filter(Site_Services.service_id == id).first()
        try:
            if siteservices:
                siteservices.remarks = data.remarks
                siteservices.services = data.services
                siteservices.updated_by_id = data.updated_by_id
                db.commit()
                return {"response": "Services Updated Successfully"}
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service not found.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
