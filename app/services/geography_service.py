from app.model.user import User
from app.model.geography import Geography
from app.model.cities import City
from app.model.md_cities import Md_Cities
from app.model.country_details import CountryDetails
from fastapi import HTTPException, status
import bcrypt
from app.db.database import get_db,SessionLocal
from sqlalchemy import func,desc
from app.model.state import State
from app.model.country_state import CountryState
from app.model.country_state_muni import CountryStateMuni
from app.model.country_state_muni_trn import CountryStateMuniTrn


class Geography_Service:
    def add_geography(self,data):
        db = next(get_db())
        geography = db.query(Geography).filter(Geography.country_code == data.country_id).first()
        city = db.query(City).filter(func.lower(City.city_name) == data.city.lower()).first()
        # if(city):
        #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="City already exists")
        # else:        
        try:
            # existing_city = db.query(City).filter(City.country_id == geography.geography_id).filter(func.lower(City.city_name) == data.city.lower()).first()
            if(geography):
                existing_city = db.query(City).filter(City.country_id == geography.geography_id).filter(func.lower(City.city_name) == data.city.lower()).first()
                if(existing_city):
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="City already exists")
                else:
                    new_city = City(
                        country_id = geography.geography_id,
                        city_name = data.city,
                        created_by_id = data.created_by_id
                    )
                    db.add(new_city)
                    db.commit()
                    db.refresh(new_city)
                    return{"response":"Geography added Successfully"}
            else:   
                new_geography = Geography(
                    country_code = data.country_id,
                    country_description = data.country_id,
                    region_code = data.country_id,
                    region_description = data.country_id,
                    created_by_id = data.created_by_id
                )        
                db.add(new_geography)
                db.commit()
                db.refresh(new_geography)

                new_existing_city = db.query(City).filter(City.country_id == data.country_id).filter(func.lower(City.city_name) == data.city.lower()).first()
                if(new_existing_city):     
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="City already exists")
                else:
                    new_city = City(
                        country_id = new_geography.geography_id,
                        city_name = data.city,
                        created_by_id = data.created_by_id
                    )
                    db.add(new_city)
                    db.commit()
                    db.refresh(new_city)
                    return{"response":"Geography added Successfully"}
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:    
            db.close()
    
    def get_geographies(self):
        db = next(get_db())
        try:
            geographies = db.query(Geography.geography_id,CountryDetails.country_code,CountryDetails.region,CountryDetails.country_name,CountryDetails.region_code,City.city_id,City.city_name).join(CountryDetails,Geography.country_code == CountryDetails.country_id).join(City,City.country_id == Geography.geography_id).order_by(desc(City.created)).all()
            return {"response":geographies}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_geography(self,geography_id,city_id):
        db= next(get_db())
        try:
            geography = db.query(Geography.geography_id,CountryDetails.country_code,CountryDetails.region,CountryDetails.country_name,CountryDetails.region_code,City.city_id,City.city_name).join(CountryDetails,Geography.country_code == CountryDetails.country_id).join(City,City.country_id == Geography.geography_id).filter(Geography.geography_id == geography_id).filter(City.city_id == city_id).all()
            return {"response":geography}   
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close() 

    def update_geography(self,id,data):
        db= next(get_db())
        city = db.query(City).filter(City.city_id == id).first()
        geography_city = db.query(City).filter(func.lower(City.city_name) == data.city.lower()).first()
        if(geography_city):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="City already exists")
        else:
            try:
                if(city):
                    city.city_name = data.city,
                    city.updated_by_id = data.updated_by_id
                    db.commit()
                    return {"response":"Geography updated Successfully"}
                else:
                    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "Geography not found")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
            finally:
                db.close()           

    def get_cities(self,id):
        db=next(get_db())
        try:
            cities = db.query(Md_Cities).filter(Md_Cities.country_id == id.upper()).all()
            return cities
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()

    def get_states(self,id):
        db=next(get_db())
        try:
            states = db.query(CountryState.country_state_id, CountryState.country_id, State.state_id, State.state_name).join(State, State.state_id == CountryState.state_id).filter(CountryState.country_id == id).all()
            return states
        finally:
            db.close() 

    def get_municipalities(self,id):
        db = next(get_db())
        try:
            municipalities = db.query(CountryStateMuni).filter(CountryStateMuni.country_state_id == id).all()
            return municipalities
        finally:
            db.close()    
    def add_municipalities(self,data):
        db = next(get_db())
        try:
            org_id = db.query(User).filter(User.id == data.created_by_id).first()
            users = db.query(User).filter(User.org_id == org_id.org_id).all()
            existing_municipality_list = []
            for user in users:
                municipalities = db.query(CountryStateMuniTrn).filter(CountryStateMuniTrn.created_by_id == user.id).all()
                if(municipalities):
                    existing_municipality_list.extend(municipalities)

            check_existing_municipality = False
            for municipality in data.municipality_id:
                if any(existing_municipality.municipality_id == municipality for existing_municipality in existing_municipality_list):
                    check_existing_municipality = True
                    break
            if(check_existing_municipality):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Municipality already exists")  
            else:          

                for municipality in data.municipality_id:
                    new_municipality = CountryStateMuniTrn(
                        municipality_id = municipality,
                        created_by_id = data.created_by_id
                    )
                    db.add(new_municipality)
                    db.commit()
                    db.refresh(new_municipality)
                return "Municipality Added Successfully"
        finally:
            db.close()

    def get_added_municipalities(self,user_id):
        db = next(get_db())
        try:
            get_data_of_user = db.query(User).filter(User.id == user_id).first()
            # get data by org, taking user_id as input paramter

            if get_data_of_user:
                if get_data_of_user.org_id:
                    list_of_users_related_to_org = db.query(User).filter(User.org_id== get_data_of_user.org_id).all()
                    # return get_list_of_users_related_to_org
                    added_municipalities =[]
                    for user in list_of_users_related_to_org:
                        municipalities = db.query(
                            CountryStateMuniTrn.country_state_muni_trn_id, CountryStateMuni.country_state_muni_id,CountryStateMuni.municipality, CountryState.country_state_id, CountryDetails.region, CountryDetails.country_id,CountryDetails.country_code,CountryDetails.region_code, CountryDetails.country_name, State.state_id, State.state_name
                        ).join(
                            CountryStateMuni,
                            CountryStateMuni.country_state_muni_id == CountryStateMuniTrn.municipality_id,
                        ).join(
                            CountryState,
                            CountryState.country_state_id == CountryStateMuni.country_state_id,
                            isouter=True,  
                        ).join(
                            CountryDetails,
                            CountryDetails.country_id == CountryState.country_id,
                            isouter=True,
                        ).join(
                            State,
                            State.state_id == CountryState.state_id,
                            isouter=True,
                        ).filter(CountryStateMuniTrn.created_by_id == user.id ).order_by(desc(CountryStateMuniTrn.created)).all()
                        
                        added_municipalities.extend(municipalities)

                    return added_municipalities
                else:
                    return {"throw":f"user_id = {user_id} is not mapped to any organization"}
            else:
                return {"catch":f"user_id = {user_id} not found"}
        finally:
            db.close()

    def update_municipality(self,id,data):
        db = next(get_db())
        try:
            municipality = db.query(CountryStateMuniTrn).filter(CountryStateMuniTrn.municipality_id == data.country_state_muni_id).first()
            if(municipality):
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Municipality already exists")  
            else:
                existing_municipality = db.query(CountryStateMuniTrn).filter(CountryStateMuniTrn.country_state_muni_trn_id == id).first()
                if(existing_municipality):
                    existing_municipality.municipality_id = data.country_state_muni_id
                    existing_municipality.updated_by_id = data.updated_by_id
                    db.commit()
                    return "Municipality Updated Successfully"
                else:
                     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="ID doesn't exists")  

        finally:
            db.close() 
    
    def get_geography_municplaities(self,id):
        db = next(get_db())
        try:
            muncipalities = db.query(CountryStateMuniTrn.municipality_id,CountryStateMuniTrn.country_state_muni_trn_id,CountryStateMuni.country_state_muni_id,CountryStateMuni.municipality)\
            .join(CountryStateMuniTrn,CountryStateMuniTrn.municipality_id==CountryStateMuni.country_state_muni_id)\
            .join(CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id )\
            .join(CountryDetails,CountryDetails.country_id == CountryState.country_id)\
            .join(State,State.state_id ==CountryState.state_id)\
            .filter(CountryState.state_id==id).all()
            return muncipalities
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
            
    def get_geography_countries(self):
        db = next(get_db())
        try:
            countries = db.query(CountryStateMuniTrn.municipality_id,CountryStateMuniTrn.country_state_muni_trn_id,CountryStateMuni.country_state_muni_id,
                CountryDetails.country_id,CountryDetails.country_name,CountryDetails.country_code,CountryDetails.region_code,CountryDetails.region,CountryStateMuni.country_state_id).distinct(CountryDetails.country_id)
            countries = countries.join(
                 CountryStateMuniTrn, CountryStateMuniTrn.municipality_id == CountryStateMuni.country_state_muni_id
            ).join(
                CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id
            )\
            .join(
                CountryDetails,CountryDetails.country_id == CountryState.country_id
            ).all()
            return countries
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
    def get_geography_states(self,id):
        db = next(get_db())
        try:
            states = db.query(CountryDetails.country_id,CountryDetails.country_name,CountryStateMuni.country_state_id,State.state_name,State.state_id)\
            .join(CountryStateMuniTrn,CountryStateMuniTrn.municipality_id==CountryStateMuni.country_state_muni_id)\
            .join(CountryState,CountryState.country_state_id ==CountryStateMuni.country_state_id )\
            .join(CountryDetails,CountryDetails.country_id == CountryState.country_id)\
            .join(State,State.state_id ==CountryState.state_id)\
            .filter(CountryState.country_id==id).distinct(State.state_id).all()
            return states
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

            
                  
