from app.model.country_details import CountryDetails
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func, asc

class Countries_Service:
    def get_country_details(self):
        db = next(get_db())
        try:
            countries = db.query(CountryDetails).order_by(asc(CountryDetails.country_name)).all()
            return countries
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
    
    def country_details(self,id):
        db = next(get_db())
        try:
            country = db.query(CountryDetails).filter(CountryDetails.country_id == id).first()
            return country
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()