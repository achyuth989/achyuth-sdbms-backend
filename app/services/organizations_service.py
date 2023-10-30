from app.model.organizations import Organizations
from app.db.database import get_db
from fastapi import HTTPException,status
from sqlalchemy import func
from app.schemas.organizations_schema import Organizations_Schema
from sqlalchemy import func,desc,and_ 
import re
from fastapi.responses import JSONResponse
from app.model.miscellaneous import Miscellaneous

class Organizations_Service():
    def add_update_organizations(self,data):
        db = next(get_db())
        try:
            org_id = data.id 
            org_name = data.org_name
            org_address = data.org_address
            
            org_status_data = db.query(Miscellaneous).filter(Miscellaneous.value == "1").first()
            
            
            if org_name is not None and org_name.strip() != "":
                org_name = data.org_name.lower().strip()
                org_name = re.sub(r'\s+', ' ', org_name)
            else:
                org_name = None
                
            if org_address is not None and org_address.strip()!="":
                org_address = data.org_address.lower()
                # formatted_address = ', '.join(word.capitalize() for word in re.split(r'[\s,]+', org_address) if word)
                org_address = re.sub(r'\s+', ' ', org_address)
            else:
                org_address = None
            
            created_by_id = data.created_by_id

            
            organizations_data = db.query(Organizations).filter(Organizations.id== org_id).first()
            if organizations_data:
                organizations_data.org_name = org_name
                organizations_data.org_address = org_address
                organizations_data.updated_by_id = created_by_id
                db.commit()
                return {"response":"organization updated successfully"}
            else:
                org_name_data = db.query(Organizations).filter(Organizations.org_name== org_name).first()
                if org_name_data:
                    return JSONResponse(
                        content={"response":f"organization name : {org_name} already exists"},
                        status_code=status.HTTP_404_NOT_FOUND,
                        headers={"Content-Type": "application/json"}  # Set the Content-Type header
                        ) 
                    # return {"response":"organization name already exists"}
                else:
                    new_organization = Organizations(
                        org_name = org_name,
                        org_address = org_address,
                        status = org_status_data.miscellaneous_id,
                        created_by_id = created_by_id
                    )
                    db.add(new_organization)
                    db.commit()
                    db.refresh(new_organization)
                    return {"response":"organization added successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:        
            db.close()
            
    def get_all_org_details(self):
        db = next(get_db())
        try:
            all_organizations = db.query(Organizations).order_by(desc(Organizations.created)).all()
            if all_organizations:
                for org in all_organizations:
                    
                    address = org.org_address
                    if address is not None and address.strip() != "":
                        # formatted_address = ', '.join(word.capitalize() for word in re.split(r'[\s,]+', address) if word)
                        # formatted_address = re.sub(r'\s+', ' ', formatted_address)
                        # removed join function which replaces space with comma(,)
                        formatted_address = address.title().strip()
                    else:
                        formatted_address = None
                    
                    
                    if org.org_name is not None and org.org_name.strip() != "":
                        name = org.org_name.title().strip()
                    else: 
                        name = None
                        
                        
                    if org.status is not None:
                        status_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == org.status).first()
                        org_status_data = status_data.value
                        
                        if org_status_data == "1":
                            org_status = "Active"
                        else:
                            org_status = "Inactive"
                    else:
                        org_status = None
                    
                    org.org_address = formatted_address
                    org.org_name = name
                    org.org_status = org_status
                return all_organizations
            else:
                return JSONResponse(
                    content={"response":f"No data found for organisations"},
                    status_code=status.HTTP_404_NOT_FOUND,
                    headers={"Content-Type": "application/json"}  # Set the Content-Type header
                    ) 
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:        
            db.close()
  
            
    def get_org_details_by_org_id(self,org_id):
        db = next(get_db())
        try:
            org_data = db.query(Organizations).filter(Organizations.id == org_id).first()
            
            if org_data:
            
                address = org_data.org_address
                if address is not None and address.strip() != "":
                    # removed join function which replaces space with comma(,)
                    formatted_address = address.title().strip()
                else:
                    formatted_address = None
                    
                if org_data.org_name is not None and org_data.org_name.strip() != "":
                    name = org_data.org_name.title()
                else:
                    name = None
                    
                if org_data.status is not None:
                    status_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == org_data.status).first()
                    org_status_data = status_data.value
                    
                    if org_status_data == "1":
                        org_status = "Active"
                    else:
                        org_status = "Inactive"
                else:
                    org_status = None
                    
                org_data.org_address = formatted_address
                org_data.org_name = name
                org_data.org_status = org_status
                
                return org_data
            else:
                return JSONResponse(
                    content={"response":f"No data found for this id={org_id} in all organisations"},
                    status_code=status.HTTP_404_NOT_FOUND,
                    headers={"Content-Type": "application/json"}  # Set the Content-Type header
                ) 

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:        
            db.close()
            
            
    def update_org_status_by_id(self,data):
        db = next(get_db())
        try:
            organisation_data = db.query(Organizations).filter(Organizations.id == data.id).first()
            
            active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
            inactive = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "0").first()
            if(organisation_data.status == active.miscellaneous_id):
                organisation_data.status = inactive.miscellaneous_id
                organisation_data.updated_by_id = data.updated_by_id
                db.commit()
                return {"response":"organisation deactivated succesfully"}
            elif(organisation_data.status == inactive.miscellaneous_id):
                organisation_data.status = active.miscellaneous_id
                organisation_data.updated_by_id = data.updated_by_id
                db.commit()
                return {"response":"organisation activated succesfully"}
            else:
                return {"response":f"status not found for this organisation = {organisation_data.org_name}"}
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
            
    def get_all_active_organizations(self):
        db = next(get_db())
        try:
            active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
            
            all_organizations = db.query(Organizations).filter(Organizations.status==active.miscellaneous_id).order_by(desc(Organizations.created)).all()
    
            if all_organizations:
                for org in all_organizations:
                    
                    address = org.org_address
                    if address is not None and address.strip() != "":
                        formatted_address = address.title()
                    else:
                        formatted_address = None
                    
                    
                    if org.org_name is not None and org.org_name.strip() != "":
                        name = org.org_name.title()
                    else: 
                        name = None
                        
                        
                    if org.status is not None:
                        status_data = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id == org.status).first()
                        org_status_data = status_data.value
                        
                        if org_status_data == "1":
                            org_status = "Active"
                        else:
                            org_status = "Inactive"
                    else:
                        org_status = None
                    
                    org.org_address = formatted_address
                    org.org_name = name
                    org.org_status = org_status
                return all_organizations
            else:
                return JSONResponse(
                    content={"response":f"No data found for organisations"},
                    status_code=status.HTTP_404_NOT_FOUND,
                    headers={"Content-Type": "application/json"}  # Set the Content-Type header
                    ) 
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:        
            db.close()
            
        
        
        
        
