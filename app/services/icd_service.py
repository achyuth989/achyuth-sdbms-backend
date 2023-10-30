from fastapi import HTTPException, status
from fastapi.logger import logger
from app.db.database import get_db
from datetime import datetime
from app.model.icd import Icd
from app.model.speciality import Speciality
from app.model.speciality_subspeciality import SpecialitySubspeciality
from sqlalchemy import text
import json
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

class Icd_Service:
    def build_tree(self, icd_codes, parent=None, level=1):
        tree = []
        for icd_code in icd_codes:
            if icd_code.parent == parent and icd_code.icd_level == level:
                children = self.build_tree(icd_codes, icd_code.icd_code, level + 1)
                node = {
                    "icd_code": icd_code.icd_code,
                    "parent": icd_code.parent,
                    "icd_id": icd_code.icd_id,
                    "description": icd_code.description,
                    "icd_level": icd_code.icd_level,
                    "children": children,
                }
                tree.append(node)
        return tree

    def get_icd_codes(self):
        db= next(get_db())
        try:
            icd_codes = db.query(Icd).limit(2550).all()
            tree = self.build_tree(icd_codes)
            return tree
        except Exception as e:
            db.rollback()
            raise HTTPException(detail=str(e))
        finally:
            db.close()
            
    def get_all_icd_codes(self):
        db= next(get_db())
        try:
            current_time = datetime.now() 
            timestamp_with_milliseconds = current_time.strftime("%Y-%m-%d %H:%M:%S.%f") 
            print("start:",timestamp_with_milliseconds)
            icd_codes = db.query(Icd).all()
            current_time = datetime.now() 
            timestamp_with_milliseconds = current_time.strftime("%Y-%m-%d %H:%M:%S.%f") 
            print("end:",timestamp_with_milliseconds)
            tree = self.build_tree(icd_codes)
            current_time = datetime.now() 
            timestamp_with_milliseconds = current_time.strftime("%Y-%m-%d %H:%M:%S.%f") 
            print("final:",timestamp_with_milliseconds)
            return tree
        except Exception as e:
            db.rollback()
            raise HTTPException(detail=str(e))
        finally:
            db.close()
            
    def get_all_icd_codes_by_querying(self):
        db= next(get_db())
        try:
            # this query failed to map all childs
            # query='''

            # SELECT

            #     ROW_NUMBER() OVER () AS "s.no",
                
            #     level1.icd_id As level1_icd_id,  
            #     level1.description AS "level1",
            #     level1.icd_code AS "level1_code",
                
            #     level2.icd_id As level2_icd_id,
            #     level2.description AS "level2",
            #     level2.icd_code AS "level2_code",

            #     level3.icd_id As level3_icd_id,
            #     level3.description AS "level3",
            #     level3.icd_code AS "level3_code",

            #     level4.icd_id As level4_icd_id,
            #     level4.description AS "level4",
            #     level4.icd_code AS "level4_code"

            # FROM icd AS level1
            # LEFT JOIN icd AS level2 ON level1.icd_code = level2.parent AND level2.icd_level = 2
            # LEFT JOIN icd AS level3 ON level2.icd_code = level3.parent AND level3.icd_level = 3
            # LEFT JOIN icd AS level4 ON level3.icd_code = level4.parent AND level4.icd_level = 4
            # ORDER BY "level4_icd_id";
            
            # '''
            
            query ='''
            

                WITH RECURSIVE ICD_Hierarchy AS (
                SELECT
                    COALESCE(level1.description, '') AS "level1",
                    COALESCE(level1.icd_code, '') AS "level1_code",
                    level1.icd_id AS "level1_icd_id",
                    COALESCE(level2.description, '') AS "level2",
                    COALESCE(level2.icd_code, '') AS "level2_code",
                    level2.icd_id AS "level2_icd_id",
                    COALESCE(level3.description, '') AS "level3",
                    COALESCE(level3.icd_code, '') AS "level3_code",
                    level3.icd_id AS "level3_icd_id",
                    COALESCE(level4.description, '') AS "level4",
                    COALESCE(level4.icd_code, '') AS "level4_code",
                    level4.icd_id AS "level4_icd_id",
                    COALESCE(level1.icd_code, '') AS "root_code",
                    level1.icd_id AS "root_id",
                    1 AS "level"
                FROM icd AS level1
                LEFT JOIN icd AS level2 ON level1.icd_code = level2.parent AND level2.icd_level = 2
                LEFT JOIN icd AS level3 ON level2.icd_code = level3.parent AND level3.icd_level = 3
                LEFT JOIN icd AS level4 ON level3.icd_code = level4.parent AND level4.icd_level = 4
                WHERE level1.icd_level = 1
                UNION ALL
                SELECT
                    H.level1,
                    H."level1_code",
                    H."level1_icd_id",
                    H.level2,
                    H."level2_code",
                    H."level2_icd_id",
                    H.level3,
                    H."level3_code",
                    H."level3_icd_id",
                    H.level4,
                    H."level4_code",
                    H."level4_icd_id",
                    C.icd_code AS "root_code",
                    C.icd_id AS "root_id",
                    H.level + 1 AS "level"
                FROM ICD_Hierarchy AS H
                INNER JOIN icd AS C ON H."level4_code" = C.parent AND C.icd_level = H.level + 1
                )
                SELECT DISTINCT
                "level1",
                "level1_code",
                "level1_icd_id",
                "level2",
                "level2_code",
                "level2_icd_id",
                "level3",
                "level3_code",
                "level3_icd_id",
                "level4",
                "level4_code",
                "level4_icd_id",
                "level",
                "root_code",
                "root_id"
                FROM ICD_Hierarchy
                ORDER BY "root_code", "level";
            
            '''
            
            
            result = db.execute(text(query)).fetchall()
            # limited_result = result[:9663]
           
            return result
        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
        
            
            
            
# new tree  not recommended

    # def build_tree(self, icd_codes, parent=None):
    #     tree = {}
    #     for icd_code in icd_codes:
    #         if icd_code.parent == parent:
    #             icd_id = icd_code.icd_id
    #             children = self.build_tree(icd_codes, icd_code.icd_code)
    #             node = {
    #                 "icd_code": icd_code.icd_code,
    #                 "parent": icd_code.parent,
    #                 "icd_id": icd_code.icd_id,
    #                 "description": icd_code.description,
    #                 "icd_level": icd_code.icd_level,
    #                 "children": children,
    #             }
    #             tree[icd_id] = node
    #     return tree
    
    # def get_icd_codes(self):
    #     db = next(get_db())
    #     try:
    #         icd_codes = db.query(Icd).limit(2550).all()
    #         tree = self.build_tree(icd_codes)
    #         return list(tree.values())
    #     except Exception as e:
    #         db.rollback()
    #         raise HTTPException(detail=str(e))
    #     finally:
    #         db.close()

    # def get_all_icd_codes(self):
    #     db = next(get_db())
    #     try:
    #         icd_codes = db.query(Icd).all()
    #         tree = self.build_tree(icd_codes)
    #         return list(tree.values())
    #     except Exception as e:
    #         db.rollback()
    #         raise HTTPException(detail=str(e))
    #     finally:
    #         db.close()
    
# new tree end not recommended



    def get_sub_speciality(self):
        db= next(get_db())
        try:
            results = db.query(SpecialitySubspeciality.id,Speciality.speciality, SpecialitySubspeciality.subspeciality).join(Speciality).all()
            return results
        except Exception as e:
            db.rollback()
            raise HTTPException(detail=str(e))
        finally:
            db.close()

    def get_sub_speciality_speciality(self):
        db= next(get_db())
        try:
            results = db.query(SpecialitySubspeciality.id,SpecialitySubspeciality.subspeciality,Speciality.speciality,Speciality.id).join(Speciality).all()
            return results
        except Exception as e:
            db.rollback()
            raise HTTPException(detail=str(e))
        finally:
            db.close()


# 25/08/2023 modified by achyuth
    
    def get_icd_codes_by_id(self,page_id):
        db= next(get_db())
        try:
            page_size = 1000
            start_offset = (page_id - 1) * page_size
            end_offset = (page_id * page_size)-1
            icd_codes = db.query(Icd).filter(Icd.icd_id.between(start_offset, end_offset)).all()
            return icd_codes
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()
    

    def get_icd_codes_by_logic(self,page_id):
        db= next(get_db())
        try:     
            # top_parents = db.query(Icd).filter(Icd.parent.is_(None)).limit(5).all()
            page_size = 2
            start_offset = (page_id - 1) * page_size
            end_offset =(page_id * page_size)-1
            top_parents =db.query(Icd).filter(Icd.icd_id.between(start_offset, end_offset)).all()
            icd_codes = []
            for parent in top_parents:
                children = self.build_tree(db.query(Icd).all(), parent.icd_code, level=2)
                node = {
                    "icd_code": parent.icd_code,
                    "parent": parent.parent,
                    "icd_id": parent.icd_id,
                    "description": parent.description,
                    "icd_level": parent.icd_level,
                    "children": children,
                }
                icd_codes.append(node)
            return icd_codes
            # icd_codes = db.query(Icd).all()
            # icd_codes = db.query(Icd).filter(Icd.icd_level == 1).limit(5).all()
            # tree = self.build_tree(icd_codes)
            # return tree
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            # raise HTTPException(detail=str(e))
        finally:
            db.close()
            
    def get_all_icds(self):
        db= next(get_db())
        try:
            all_icds = db.query(Icd).all()
            return all_icds
        
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            db.close()

    