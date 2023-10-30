from app.model.regulatory_info_site_rec import RegulatoryInfo
from app.model.documents import Documents
from app.model.document_category import DocumentCategory
from app.model.miscellaneous import Miscellaneous
# from app.model.questionary import Questionary
from app.db.database import get_db
from  fastapi import HTTPException,status
from sqlalchemy import func
from app.schemas.regulatory_info_site_rec import Regulatory_Information,Documents_List,Update_Regulatory_Information

class Regulatory_Info_Service:
    def add_regulatory_info_details(self,regulatory_info):
        db = next(get_db())
        try:
            # Get the site_id of the newly inserted crinfo
            for document in regulatory_info.documents:
                new_reg_info = RegulatoryInfo(
                    site_id = regulatory_info.site_id,
                    document_category_id = document.document_category_id,
                    document = document.document,
                    availability =document.availability,
                    date= document.date,
                    remarks= document.remarks,
                    # documents=regulatory_info.document,
                    created_by_id = regulatory_info.created_by_id
                )
                db.add(new_reg_info)
                db.commit()
                db.refresh(new_reg_info)
            return {"Regulatory info details added succesfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

            
    def update_regulatory_info_details(self,site_rec_reg_info_id:int,update_reg_info:Update_Regulatory_Information,regulatory_info:Regulatory_Information):
        db = next(get_db())
        try:
            for document in regulatory_info.documents:
                if document.site_rec_reg_info_id == site_rec_reg_info_id:
                    update_reg_infor = db.query(RegulatoryInfo).filter(RegulatoryInfo.site_rec_reg_info_id == site_rec_reg_info_id).first()
                    if update_reg_infor:
                        update_reg_infor.document = update_reg_info.document,
                        update_reg_infor.availability = update_reg_info.availability,
                        update_reg_infor.date = update_reg_info.date,
                        update_reg_infor.remarks = update_reg_info.remarks,
                        update_reg_infor.updated_by_id = update_reg_info.updated_by_id
                        db.commit()
            return{"response":"Document_updated sucessfully"}

            # return update_reg_info
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
        finally:
            db.close()
            
            
    def delete_regulatory_info_details_by_site_id_and_site_rec_reg_info_id(self,site_id,site_rec_reg_info_id):
        db = next(get_db()) 
        try:
            regulatory_info_details = db.query(RegulatoryInfo).filter(RegulatoryInfo.site_id == site_id).filter(RegulatoryInfo.site_rec_reg_info_id == site_rec_reg_info_id).first()
            if regulatory_info_details:
                db.delete(regulatory_info_details)
                db.commit()
                return "regulatory_info_details deleted successfully"
            else:
                return f"site_id={site_id} or site_rec_reg_info_id = {site_rec_reg_info_id} is invalid"
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
            
    
    # def add_or_update_regulatory_info_details(self,regulatory_info,update_reg_info):
    #     pass
        # site_rec_reg_info_id = regulatory_info.site_rec_reg_info_id
        # if site_rec_reg_info_id == 0:
        #     # add_regulatory_info_details(self,regulatory_info)
        #     return "new record"
        # else:
        #     # update_regulatory_info_details(self,update_reg_info,regulatory_info,site_rec_reg_info_id)
        #     return "existing record"
            
        


    def get_all_regulatory_info_details(self):
        db = next(get_db())
        try:
            regulatory_info_details = db.query(RegulatoryInfo).all()
            all_records =[]
            for details in regulatory_info_details:
                document_category_record = db.query(DocumentCategory).filter(DocumentCategory.document_category_id== details.document_category_id).first()
                if document_category_record:
                    details.document_category_description = document_category_record.description
                else:
                    details.document_category_description = None
                    
                status_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id== details.availability).first()
                if status_record:
                    details.document_status = status_record.value
                else:
                    details.document_status = None
                    
                all_records.append(details)
                    
                
            return all_records
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

        
    def get_regulatory_info_details_by_site_id(self,site_id):
        db = next(get_db())
        try:
            regulatory_info_details = db.query(RegulatoryInfo).filter(RegulatoryInfo.site_id == site_id).all()
            if regulatory_info_details:
                all_records = []
                for details in regulatory_info_details:
                    document_category_record = db.query(DocumentCategory).filter(DocumentCategory.document_category_id== details.document_category_id).first()
                    if document_category_record:
                        details.document_category_description = document_category_record.description
                    else:
                        details.document_category_description = None
                        
                    status_record = db.query(Miscellaneous).filter(Miscellaneous.miscellaneous_id== details.availability).first()
                    if status_record:
                        details.document_status = status_record.value
                    else:
                        details.document_status = None
                    # details.document_category_description = document_category_record.description
                    # details.document_status = status_record.value
                
                    
                    all_records.append(details)
                return all_records
            else:
                return "please enter a valid site id"
            return regulatory_info_details
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
        finally:
            db.close()
            
    # def update_regulatory_info_details_by_site_id_and_document_id(self,site_id,document_id,reg_info):
    #     db = next(get_db())
    #     update_reg_info = db.query(RegulatoryInfo).filter(RegulatoryInfo.site_id == site_id, RegulatoryInfo.document==document_id).first()
    #     try:
    #         if(update_reg_info):
    #             # update_reg_info.document = reg_info.document,
    #             update_reg_info.availability = reg_info.availability
    #             update_reg_info.date = reg_info.date
    #             update_reg_info.remarks = reg_info.remarks
    #             update_reg_info.updated_by_id = reg_info.updated_by_id
    #             db.commit()

    #             return{"response":f"Document_id={document_id} for site_id={site_id} updated sucessfully"}
    #             # return update_reg_info
    #         else:
    #             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Regulatory info not found.")
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    #     finally:
    #         db.close()
            
    
    
    # def edit_cr_infra(self, site_id: int, cr_infra_edit: Cr_infra):
    #     db = next(get_db())
    #     try:
    #         cr_infra = db.query(Cr_infra).filter(Cr_infra.site_id == site_id).first()
    #         if not it:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cr infra questionary not found")
    #         cr_infra.question = cr_infra_edit.question
    #         cr_infra.answer = cr_infra_edit.answer
    #         cr_infra.updated_by_id = cr_infra_edit.updated_by_id
    #         cr_infra.updated = datetime.now()

    #         db.commit()
    #         db.refresh(it)
    #         return {"response": "Cr infra questionary updated successfully"}
    #     except Exception as e:
    #         db.rollback()
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    #     finally:
    #         db.close()





            
            
            
            
            
# try:
#     pass
# except Exception as e:
#     db.rollback()
#     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
# finally:
#     db.close()



