from app.model.user import User
from sqlalchemy import select
from app.model.institution import Institution
from app.model.miscellaneous import Miscellaneous
from app.model.contacts import Contacts
from app.model.country_state_muni_trn import CountryStateMuniTrn
from app.model.country_state_muni import CountryStateMuni
from app.model.country_state import CountryState
from app.model.state import State
from app.model.country_state_muni_trn import CountryStateMuniTrn
from app.model.country_state_muni import CountryStateMuni
from app.model.country_state import CountryState
from app.model.state import State
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from app.model.notes import Note
from app.model.cities import City
from app.model.geography import Geography
from app.model.country_details import CountryDetails
from sqlalchemy import desc
from sqlalchemy import func
from app.model.site import Site

class Institution_Service:
    def add_institution(self,data):
        db = next(get_db())
        session=SessionLocal()
        org_id = db.query(User).filter(User.id == data.created_by_id).first()
        users = db.query(User).filter(User.org_id == org_id.org_id).all()
        existing_institution_list = []
        for user in users:
            institutions = db.query(Institution).filter(Institution.created_by_id == user.id).all()
            if(institutions):
                existing_institution_list.extend(institutions)
        check_existing_institution = False
        if any(existing_institution.institution_code.lower() == data.institution_code.lower() for existing_institution in existing_institution_list):
            check_existing_institution = True
        try:
            # email = db.query(Institution).filter(Institution.email == data.email).first()
            # phone = db.query(Institution).filter(Institution.mobile_number == data.mobile_number).first()
            institution_code = db.query(Institution).filter(func.lower(Institution.institution_code) == data.institution_code.lower()).first()
            if(check_existing_institution):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Institution code already exists")\
                
            else:
                results = session.query(Miscellaneous).all()
                results = session.query(Miscellaneous).filter(Miscellaneous.value == "1").first()
                new_institution = Institution(
                    institution_code = data.institution_code,
                    institution_name = data.institution_name,
                    address_1 = data.address_1,
                    address_2 = data.address_2,
                    address_3 = data.address_3,
                    address_4 = data.address_4,
                    # city = data.city,
                    country_state_muni_trn_id = data.country_state_muni_trn_id,
                    # state= data.state,
                    district = data.district,
                    region = data.region,
                    pin_code = data.pincode,
                    # country = data.country,
                    website = data.website,
                    status = results.miscellaneous_id,
                    created_by_id = data.created_by_id
                )
                db.add(new_institution)        
                db.commit()
                db.refresh(new_institution) 

                smo_contact_list = []
                for contact_data in data.smo_contacts:
                    new_smo_contact = Contacts(  
                        capture_id = new_institution.institution_id,
                        screen_capture = "institution-smo",
                        contact_name = contact_data.contact_name,
                        role = contact_data.role,
                        office_telephone = contact_data.office_telephone,
                        extension = contact_data.extension,
                        mobile_number = contact_data.mobile_number,
                        email = contact_data.email,
                        created_by_id = data.created_by_id
                    )
                    smo_contact_list.append(new_smo_contact)
                db.add_all(smo_contact_list)     
                db.commit() 
                for contact in smo_contact_list:
                    db.refresh(contact) 

                institution_contact_list = []
                for contact_data in data.institution_contacts:
                    new_institution_contact = Contacts(  
                        capture_id = new_institution.institution_id,
                        screen_capture = "institution",
                        contact_name = contact_data.contact_name,
                        role = contact_data.role,
                        office_telephone = contact_data.office_telephone,
                        extension = contact_data.extension,
                        mobile_number = contact_data.mobile_number,
                        email = contact_data.email,
                        created_by_id = data.created_by_id
                    )
                    institution_contact_list.append(new_institution_contact)
                db.add_all(institution_contact_list)     
                db.commit() 
                for contact in institution_contact_list:
                    db.refresh(contact)           
                user_type='institution'
                notes = Note(
                    type = user_type,
                    description = data.notes,
                    entity_id = new_institution.institution_id,
                    created_by_id = data.created_by_id
                )
                db.add(notes)
                db.commit()
                db.refresh(notes)
                return{"result":"Institution Added Successfully"}
        except HTTPException as http_exception:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Institution code already exists")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()        

    # def get_institution_details(self):
    #     db = next(get_db())
    #     try:
    #         detail = db.query(Institution.institution_id,Institution.institution_code,Institution.institution_name,Institution.address_1,Institution.address_2,Institution.address_3,
    #         Institution.address_4,Institution.district,Institution.region,Institution.pin_code,Institution.website,Institution.country_state_muni_id,Note.description,Miscellaneous.value,
    #         City.city_name,City.city_id,Geography.geography_id,CountryDetails.country_name,CountryStateMuniTrn.municipality_id,CountryStateMuni.municipality,
    #         State.state_name)\
    #         .join(Note, Institution.institution_id == Note.entity_id)\
    #         .join(Miscellaneous, Institution.status == Miscellaneous.miscellaneous_id)\
    #         .join(City, Institution.city == City.city_id)\
    #         .join(Geography, Institution.country == Geography.geography_id)\
    #         .join(CountryDetails, Geography.country_code == CountryDetails.country_id)\
    #         .join(CountryStateMuniTrn, Institution.country_state_muni_id == CountryStateMuniTrn.country_state_muni_trn_id)\
    #         .join(CountryStateMuni,CountryStateMuniTrn.municipality_id == CountryStateMuni.country_state_muni_id)\
    #         .filter(Note.type == "institution").order_by(desc(Institution.created)).all()        
    #         return{"response":detail}
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    #     finally:
    #         db.close()
    
    def get_institution_details(self,user_id):
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()       
        orgs=db.query(User).filter(User.org_id ==user.org_id).all()
        user_ids = [user.id for user in orgs]
        try:
            detail = db.query(Institution.institution_id,Institution.institution_code,Institution.institution_name,Institution.address_1,Institution.address_2,Institution.address_3,
            Institution.address_4,Institution.district,Institution.region,Institution.pin_code,Institution.website,Institution.country_state_muni_trn_id,Note.description,Miscellaneous.value,
            CountryDetails.country_name,CountryDetails.country_code,CountryDetails.country_id,CountryStateMuniTrn.municipality_id,CountryStateMuni.municipality,
            State.state_name,State.state_id)\
            .join(Note, Institution.institution_id == Note.entity_id)\
            .join(Miscellaneous, Institution.status == Miscellaneous.miscellaneous_id)\
            .join(CountryStateMuniTrn, Institution.country_state_muni_trn_id == CountryStateMuniTrn.country_state_muni_trn_id)\
            .join(CountryStateMuni,CountryStateMuniTrn.municipality_id == CountryStateMuni.country_state_muni_id)\
            .join(CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id )\
            .join(CountryDetails,CountryDetails.country_id == CountryState.country_id)\
            .join(State,State.state_id ==CountryState.state_id)\
            .filter(Institution.created_by_id.in_(user_ids))\
            .filter(Note.type == "institution").order_by(desc(Institution.created)).all()        
            return{"response":detail}
        finally:
            db.close()

    def institution_details(self,id):
        db = next(get_db())
        try:
            detail = db.query(Institution.institution_id,Institution.institution_code,Institution.institution_name,Institution.address_1,Institution.address_2,Institution.address_3,
            Institution.address_4,Institution.district,Institution.region,Institution.pin_code,Institution.website,Note.description,Miscellaneous.value,Institution.country_state_muni_trn_id,
            CountryDetails.country_name,CountryDetails.country_code,CountryDetails.country_id,CountryStateMuniTrn.municipality_id,CountryStateMuni.municipality,State.state_name,State.state_id)\
            .join(Note, Institution.institution_id == Note.entity_id)\
            .join(Miscellaneous, Institution.status == Miscellaneous.miscellaneous_id)\
            .join(CountryStateMuniTrn, Institution.country_state_muni_trn_id == CountryStateMuniTrn.country_state_muni_trn_id)\
            .join(CountryStateMuni,CountryStateMuniTrn.municipality_id == CountryStateMuni.country_state_muni_id)\
            .join(CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id )\
            .join(CountryDetails,CountryDetails.country_id == CountryState.country_id)\
            .join(State,State.state_id ==CountryState.state_id)\
            .filter(Institution.institution_id == id).filter(Note.type == "institution").all()
            smo_contacts = db.query(Contacts).filter(Contacts.capture_id == id).filter(Contacts.screen_capture == "institution-smo").all()
            inst_contacts = db.query(Contacts).filter(Contacts.capture_id == id).filter(Contacts.screen_capture == "institution").all()
            
            detail_dict = dict(detail[0])
            detail_dict['smo_contacts'] = smo_contacts
            detail_dict['inst_contacts'] = inst_contacts

            return detail_dict
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

  
    def update_institution_details(self,id,data):
        db = next(get_db())
        institution = db.query(Institution).filter(Institution.institution_id == id).first()
        notes = db.query(Note).filter(Note.entity_id == id).filter(Note.type == "institution").first()
        try:
            if(institution):
                institution.address_1 = data.address_1,
                institution.address_2 = data.address_2,
                institution.address_3 = data.address_3,
                institution.address_4 = data.address_4,
                # institution.city = data.city,
                institution.district = data.district,
                institution.country_state_muni_trn_id = data.country_state_muni_trn_id
                institution.region = data.region,
                institution.pin_code = data.pincode,
                # institution.country = data.country,
                institution.website = data.website,
                institution.updated_by_id = data.updated_by_id

                notes.description = data.notes
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
                            screen_capture = "institution-smo",
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

                for contact in data.institution_contacts:
                    institution_contacts = db.query(Contacts).filter(Contacts.contact_id == contact.contact_id).first()
                    if(institution_contacts):
                        institution_contacts.contact_name = contact.contact_name,
                        institution_contacts.role = contact.role,
                        institution_contacts.office_telephone = contact.office_telephone,
                        institution_contacts.mobile_number = contact.mobile_number,
                        institution_contacts.extension = contact.extension,
                        institution_contacts.email = contact.email,
                        institution_contacts.updated_by_id = data.updated_by_id
                        db.commit()
                    else:
                        new_institution_contact = Contacts(  
                            capture_id = id,
                            screen_capture = "institution",
                            contact_name = contact.contact_name,
                            role = contact.role,
                            office_telephone = contact.office_telephone,
                            extension = contact.extension,
                            mobile_number = contact.mobile_number,
                            email = contact.email,
                            created_by_id = data.updated_by_id
                        )
                        db.add(new_institution_contact)
                        db.commit()

                db.commit()                
                return{"response":"Institution updated Successfully"}
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Institution not found")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_geographycountries(self):
        db = next(get_db())
        try:
            countries = db.query(Geography.geography_id,CountryDetails.country_name,CountryDetails.country_code,CountryDetails.region,CountryDetails.region_code).join(CountryDetails, CountryDetails.country_id == Geography.country_code).all()
            return countries
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()   
                 
    

    def get_cities(self,id):
        db = next(get_db())
        try:
            cities = db.query(City).filter(City.country_id == id).all()
            return cities
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()   

    def delete_contact(self,id):
        db = next(get_db())
        try:
            contact = db.query(Contacts).filter(Contacts.contact_id == id).first()
            if(contact):
                db.delete(contact)
                db.commit()
                return "Contact deleted Successfully"
            else:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="contact id doesn't exists")    
        finally:
            db.close()   

    def update_institution_status(self,id,data):
        db = next(get_db())
        try:
            institution = db.query(Institution).filter(Institution.institution_id == id).first()
            active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
            inactive = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "0").first()
            sites = db.query(Site).filter(Site.institution_id == id).all()
            if(institution.status == active.miscellaneous_id):
                institution.status = inactive.miscellaneous_id
                institution.updated_by_id = data.updated_by_id
                db.commit()
                for site in sites:
                    site.status = inactive.miscellaneous_id
                    db.commit()
            elif(institution.status == inactive.miscellaneous_id):
                institution.status = active.miscellaneous_id 
                institution.updated_by_id = data.updated_by_id
                db.commit()  
                for site in sites:
                    site.status = active.miscellaneous_id
                    db.commit()

            return "Institution Status Updated Successfully"
        finally:
            db.close()  

    def get_active_institution_details(self):
        db = next(get_db())
        try:
            active = db.query(Miscellaneous).filter(Miscellaneous.type == "status").filter(Miscellaneous.value == "1").first()
            detail = db.query(Institution.institution_id,Institution.institution_code,Institution.institution_name,Institution.address_1,Institution.address_2,Institution.address_3,Institution.address_4,Institution.district,Institution.region,Institution.pin_code,Institution.website,Note.description,Miscellaneous.value,Institution.country_state_muni_trn_id,
            CountryDetails.country_name,CountryDetails.country_code,CountryDetails.country_id,CountryStateMuniTrn.municipality_id,CountryStateMuni.municipality,State.state_name,State.state_id)\
            .join(Note, Institution.institution_id == Note.entity_id)\
            .join(Miscellaneous, Institution.status == Miscellaneous.miscellaneous_id)\
            .join(CountryStateMuniTrn, Institution.country_state_muni_trn_id == CountryStateMuniTrn.country_state_muni_trn_id)\
            .join(CountryStateMuni,CountryStateMuniTrn.municipality_id == CountryStateMuni.country_state_muni_id)\
            .join(CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id )\
            .join(CountryDetails,CountryDetails.country_id == CountryState.country_id)\
            .join(State,State.state_id ==CountryState.state_id)\
            .filter(Institution.status == active.miscellaneous_id)\
            .filter(Note.type == "institution").order_by(desc(Institution.created)).all()        
            return{"response":detail}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

