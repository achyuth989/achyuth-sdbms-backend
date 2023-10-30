from app.model.site import Site
from app.model.notes import Note
from app.model.miscellaneous import Miscellaneous
from app.model.institution import Institution
from app.model.sales_employees import SalesEmployees
from app.model.cities import City
from app.model.geography import Geography
from app.model.country_details import CountryDetails
from app.model.contacts import Contacts
from app.model.country_state_muni_trn import CountryStateMuniTrn
from app.model.country_state_muni import CountryStateMuni
from app.model.country_state import CountryState
from app.model.state import State
from fastapi import HTTPException, status
from app.db.database import get_db
from sqlalchemy import and_ , func,desc
from app.model.user import User

class Site_Service:
    def add_site(self, site_details):
        db = next(get_db())
        org_id = db.query(User).filter(User.id == site_details.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_site_list = []
        for user in users:
            sites = db.query(Site).filter(Site.created_by_id == user.id).all()
            if(sites):
                existing_site_list.extend(sites)
        check_existing_site = False
        if any(existing_site.site_code.lower() == site_details.site_code.lower() for existing_site in existing_site_list):
            check_existing_site = True
        site_id = db.query(Site).filter(func.lower(Site.site_code) == site_details.site_code.lower()).first()
        # site_email = db.query(Site).filter(Site.email == site_details.email).first()
        # site_phone = db.query(Site).filter(Site.mobile_number == site_details.mobile_number).first()
        try:
            if (check_existing_site):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Site code already exist.")
            # elif (site_phone):
            #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Phone number already exist.")
            # elif (site_email):
            #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email Id already exist.")
            else:
                miscellaneous_list = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "1")).first()
                site_rec_status_list = db.query(Miscellaneous).filter(and_(Miscellaneous.type == "status", Miscellaneous.value == "Not Started")).first()
                new_site = Site(
                    site_code = site_details.site_code,
                    site_name = site_details.site_name,
                    institution_id = site_details.institution_id,
                    address_1 = site_details.address_1,
                    address_2 = site_details.address_2,
                    address_3 = site_details.address_3,
                    address_4 = site_details.address_4,
                    # city = site_details.city,
                    district = site_details.district,
                    region = site_details.region,
                    pin_code = site_details.pin_code,
                    country_state_muni_trn_id = site_details.country_state_muni_trn_id,
                    # country = site_details.country,
                    website = site_details.website,
                    # responsible_sales_representative = site_details.responsible_sales_representative,
                    site_rec_status = site_rec_status_list.miscellaneous_id,
                    status = miscellaneous_list.miscellaneous_id,
                    created_by_id = site_details.created_by_id        
                )
                db.add(new_site)
                db.commit()
                db.refresh(new_site)

                smo_contact_list = []
                for contact_data in site_details.smo_contacts:
                    new_smo_contact = Contacts(  
                        capture_id = new_site.site_id,
                        screen_capture = "site-smo",
                        contact_name = contact_data.contact_name,
                        role = contact_data.role,
                        office_telephone = contact_data.office_telephone,
                        extension = contact_data.extension,
                        mobile_number = contact_data.mobile_number,
                        email = contact_data.email,
                        created_by_id = site_details.created_by_id
                    )
                    smo_contact_list.append(new_smo_contact)
                db.add_all(smo_contact_list)     
                db.commit() 
                for contact in smo_contact_list:
                    db.refresh(contact) 
                site_contact_list = []
                for contact_data in site_details.site_contacts:
                    new_site_contact = Contacts(  
                        capture_id = new_site.site_id,
                        screen_capture = "site",
                        contact_name = contact_data.contact_name,
                        role = contact_data.role,
                        office_telephone = contact_data.office_telephone,
                        extension = contact_data.extension,
                        mobile_number = contact_data.mobile_number,
                        email = contact_data.email,
                        created_by_id = site_details.created_by_id
                    )
                    site_contact_list.append(new_site_contact)
                db.add_all(site_contact_list)     
                db.commit() 
                for contact in site_contact_list:
                    db.refresh(contact)          
                user_type = 'site'
                new_notes = Note(
                    type = user_type,
                    description = site_details.notes,
                    entity_id = new_site.site_id,
                    created_by_id = site_details.created_by_id
                )
                db.add(new_notes)
                db.commit()
                db.refresh(new_notes)
                return {"success": "Site added successfully." }
        finally:
            db.close()
    def sites_list(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()       
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]
        try:
            sites_list_details = db.query(Site.site_id,Site.country_state_muni_trn_id,Site.site_code,Site.site_name,Site.address_1,Site.address_2,Site.address_3,Site.address_4,Site.district,Site.region,Site.pin_code,Site.website,Note.description,Miscellaneous.value,Institution.institution_id,Institution.institution_name,CountryDetails.country_name,CountryDetails.country_code,CountryDetails.country_id,CountryStateMuniTrn.municipality_id,CountryStateMuni.municipality,State.state_name,State.state_id)\
            .join(Note, Site.site_id == Note.entity_id)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.status)\
            .outerjoin(Institution, Institution.institution_id == Site.institution_id)\
            .join(CountryStateMuniTrn, Site.country_state_muni_trn_id == CountryStateMuniTrn.country_state_muni_trn_id)\
            .join(CountryStateMuni,CountryStateMuniTrn.municipality_id == CountryStateMuni.country_state_muni_id)\
            .join(CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id )\
            .join(CountryDetails,CountryDetails.country_id == CountryState.country_id)\
            .join(State,State.state_id ==CountryState.state_id)\
            .filter(Site.created_by_id.in_(user_ids))\
            .filter(Note.type == "site").order_by(desc(Site.created)).all()
            return {"sites_list" : sites_list_details}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_sites_list_by_id(self,id):
        db = next(get_db())
        try:
            site = db.query(Site).filter(Site.site_id == id).first()
            institution_id = site.institution_id
            
            siteslist = db.query(Site.site_id,Site.site_code,Site.site_name,Site.country_state_muni_trn_id,Site.address_1,Site.address_2,Site.address_3,Site.address_4,Site.district,Site.region,Site.pin_code,Site.website,Note.description,Miscellaneous.value,Institution.institution_id,Institution.institution_name,CountryDetails.country_name,CountryDetails.country_code,CountryDetails.country_id,CountryStateMuniTrn.municipality_id,CountryStateMuni.municipality,State.state_name,State.state_id)\
            .join(Note, Site.site_id == Note.entity_id)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.status)\
            .outerjoin(Institution, Institution.institution_id == Site.institution_id)\
            .join(CountryStateMuniTrn, Site.country_state_muni_trn_id == CountryStateMuniTrn.country_state_muni_trn_id)\
            .join(CountryStateMuni,CountryStateMuniTrn.municipality_id == CountryStateMuni.country_state_muni_id)\
            .join(CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id )\
            .join(CountryDetails,CountryDetails.country_id == CountryState.country_id)\
            .join(State,State.state_id ==CountryState.state_id)\
            .filter(Site.site_id == id).filter(Note.type == "site").all()
            smo_contacts = db.query(Contacts).filter(Contacts.capture_id == id).filter(Contacts.screen_capture == "site-smo").all()
            inst_contacts = db.query(Contacts).filter(Contacts.capture_id == institution_id).filter(Contacts.screen_capture == "institution").all()
            site_contacts = db.query(Contacts).filter(Contacts.capture_id == id).filter(Contacts.screen_capture == "site").all()

            site_details = dict(siteslist[0])

            site_details['smo_contacts'] = smo_contacts
            site_details['inst_contacts'] = inst_contacts
            site_details['site_contacts'] = site_contacts

            return site_details
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
       
    def update_site(self,id,data):
        db = next(get_db())
        site = db.query(Site).filter(Site.site_id == id).first()
        notes = db.query(Note).filter(Note.entity_id == id).filter(Note.type == "site").first()
        try:
            if(site):
                site.institution_id = data.institution_id,
                site.address_1 = data.address_1,
                site.address_2 = data.address_2,
                site.address_3 = data.address_3,
                site.address_4 = data.address_4,
                # site.city = data.city,
                site.district = data.district,
                site.country_state_muni_trn_id = data.country_state_muni_trn_id
                site.region = data.region,
                site.pin_code = data.pin_code,
                # site.country = data.country,
                site.website = data.website,
                # site.responsible_sales_representative = data.responsible_sales_representative,
                site.updated_by_id = data.updated_by_id,

                notes.description = data.notes,
                notes.updated_by_id = data.updated_by_id   
                for contact in data.smo_contacts:
                    smo_contact = db.query(Contacts).filter(Contacts.contact_id == contact.contact_id).first()
                    if(smo_contact):
                        smo_contact.contact_name = contact.contact_name,
                        smo_contact.role = contact.role,
                        smo_contact.office_telephone = contact.office_telephone,
                        smo_contact.mobile_number = contact.mobile_number,
                        smo_contact.extension = contact.extension,
                        smo_contact.email = contact.email,
                        smo_contact.updated_by_id = data.updated_by_id
                        db.commit()
                    else:
                        new_smo_contact = Contacts(  
                            capture_id = id,
                            screen_capture = "site-smo",
                            contact_name = contact.contact_name,
                            role = contact.role,
                            office_telephone = contact.office_telephone,
                            extension = contact.extension,
                            mobile_number = contact.mobile_number,
                            email = contact.email,
                            created_by_id = data.updated_by_id
                        )
                        db.add(new_smo_contact)
                        db.commit()

                for contact in data.site_contacts:
                    site_contacts = db.query(Contacts).filter(Contacts.contact_id == contact.contact_id).first()
                    if(site_contacts):
                        site_contacts.contact_name = contact.contact_name,
                        site_contacts.role = contact.role,
                        site_contacts.office_telephone = contact.office_telephone,
                        site_contacts.mobile_number = contact.mobile_number,
                        site_contacts.extension = contact.extension,
                        site_contacts.email = contact.email,
                        site_contacts.updated_by_id = data.updated_by_id
                        db.commit()

                    else:
                        new_site_contact = Contacts(  
                            capture_id = id,
                            screen_capture = "site",
                            contact_name = contact.contact_name,
                            role = contact.role,
                            office_telephone = contact.office_telephone,
                            extension = contact.extension,
                            mobile_number = contact.mobile_number,
                            email = contact.email,
                            created_by_id = data.updated_by_id
                        )
                        db.add(new_site_contact)
                        db.commit()

                db.commit()
                return{"response":"Site updated Successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Site not found")
        except HTTPException as e:
            db.rollback()
            raise e  
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
    def get_institution_contacts_by_id(self, id):
        db = next(get_db())
        try:
            inst_contacts = db.query(Contacts).filter(Contacts.capture_id == id).filter(Contacts.screen_capture == "institution").all()
            if inst_contacts:
                return {"contacts" : inst_contacts}
            else :
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Institution id does not exist.")
        finally:
            db.close()

    def update_site_status(self,id,data):
        db = next(get_db())
        try:
            site = db.query(Site).filter(Site.site_id == id).first()
            active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
            inactive = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "0").first()
            institution = db.query(Institution).filter(Institution.institution_id == site.institution_id).first()

            if(site.status == active.miscellaneous_id):
                site.status = inactive.miscellaneous_id,
                site.updated_by_id = data.updated_by_id
                db.commit()
            elif(site.status == inactive.miscellaneous_id):
                if(institution):
                    if(institution.status == inactive.miscellaneous_id):
                        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Site can't be Activated as the Institution is Inactive.")
                else:        
                    site.status = active.miscellaneous_id 
                    site.updated_by_id = data.updated_by_id
                    db.commit()  

            return "Site Status Updated Successfully"
        finally:
            db.close()    
    def active_sites_list(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()       
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]
        try:
            sites_list_details = db.query(Site.site_id,Site.site_code,Site.site_name,Site.address_1,Site.address_2,Site.address_3,Site.address_4,Site.district,Site.region,Site.pin_code,Site.website,Note.description,Miscellaneous.value,Institution.institution_id,Institution.institution_name,CountryDetails.country_name,CountryDetails.country_code,CountryDetails.country_id,CountryStateMuniTrn.municipality_id,CountryStateMuni.municipality,State.state_name,State.state_id)\
            .join(Note, Site.site_id == Note.entity_id)\
            .join(Miscellaneous, Miscellaneous.miscellaneous_id == Site.status)\
            .outerjoin(Institution, Institution.institution_id == Site.institution_id)\
            .join(CountryStateMuniTrn, Site.country_state_muni_trn_id == CountryStateMuniTrn.country_state_muni_trn_id)\
            .join(CountryStateMuni,CountryStateMuniTrn.municipality_id == CountryStateMuni.country_state_muni_id)\
            .join(CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id )\
            .join(CountryDetails,CountryDetails.country_id == CountryState.country_id)\
            .join(State,State.state_id ==CountryState.state_id)\
            .filter(Site.status ==1)\
            .filter(Site.created_by_id.in_(user_ids))\
            .filter(Note.type == "site").order_by(desc(Site.created)).all()
            return {"sites_list" : sites_list_details}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()    
            
       
    
