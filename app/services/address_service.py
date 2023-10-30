from app.model.address import Address
from app.model.site import Site
from app.model.notes import Note
from app.model.miscellaneous import Miscellaneous
from app.model.institution import Institution
from app.model.sales_employees import SalesEmployees
from app.model.cities import City
from app.model.geography import Geography
from app.model.country_details import CountryDetails
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func

class Address_Service:
    def add_address(self,data):
        db = next(get_db())
        try:
            new_address = Address(
                site_id = data.site_id,
                as_per_license = data.as_per_license,
                address_1 = data.address_1,
                address_2 = data.address_2,
                address_3 = data.address_3,
                address_4 = data.address_4,
                city = data.city,
                district = data.district,
                region = data.region,
                pincode = data.pincode,
                country =data.country,
                created_by_id = data.created_by_id
            ) 
            db.add(new_address)
            db.commit()
            db.refresh(new_address)
            return {"response":"Address added Successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create address.")
        finally:
            db.close()

    def get_address(self,id):
        db = next(get_db())   
        try:
            address = db.query(Address.site_id,Address.as_per_license,Address.address_1,Address.address_2,Address.address_3,Address.address_4,Address.district,Address.pincode,Address.site_address_id, Geography.geography_id, CountryDetails.country_code,CountryDetails.region_code,CountryDetails.country_name,CountryDetails.region, City.city_id,City.city_name) \
            .outerjoin(City, City.city_id == Address.city) \
            .outerjoin(Geography, Geography.geography_id == Address.country) \
            .outerjoin(CountryDetails, Geography.country_code == CountryDetails.country_id) \
            .filter(Address.site_id == id) \
            .all()
            return address
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()     

        