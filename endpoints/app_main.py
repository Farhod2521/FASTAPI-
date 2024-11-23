from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from database import get_db
from models import Materials, MMechano, Techno
from schemas import MaterialAdsSchema, MaterialsSchema


from typing import List, Optional
from datetime import datetime
from sqlalchemy import case
from sqlalchemy import func


app_main_router =  APIRouter(tags=["Main"])

@app_main_router.get("/global/search/", response_model=dict)
async def global_search(
    name_value: Optional[str] = None,
    category: Optional[str]= None,
    page: int = 1,
    limit: int = 12,
    db: Session = Depends(get_db),
):
    page = max(page, 1)
    limit = max(limit, 1)
    offset = (page - 1) * limit
    
    if category == "material":
        query = db.query(Materials)
        
        if name_value:
            query = query.filter(Materials.material_name.ilike(f"%{name_value}%"))
            query = query.order_by(
                case((Materials.material_name.ilike(f"{name_value}%"), 1), else_=2),
                Materials.material_name,
            )
        else:
            query = query.order_by(Materials.material_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()
        
        print(f"Query Params - name_value: {name_value}, category: {category}, page: {page}, limit: {limit}")
        print(f"Retrieved Data: {all_data}")
        
        if count == 0:
            return {"count": 0, "materials": []}
        
        result = {
            "count": count,
            "materials": [
                {
                    "material_csr_code": mat.material_csr_code,
                    "material_name": mat.material_name,
                }
                for mat in all_data
            ],
        }
        return result

    elif category == "mmechno":
        query = db.query(MMechano)
        
        if name_value:
            query = query.filter(MMechano.mmechano_name.ilike(f"%{name_value}%"))
            query = query.order_by(
                case((MMechano.mmechano_name.ilike(f"{name_value}%"), 1), else_=2),
                MMechano.mmechano_name,
            )
        else:
            query = query.order_by(MMechano.mmechano_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()
        
        print(f"Query Params - name_value: {name_value}, category: {category}, page: {page}, limit: {limit}")
        print(f"Retrieved Data: {all_data}")
        
        if count == 0:
            return {"count": 0, "mmechno": []}
        
        result = {
            "count": count,
            "materials": [
                {
                    "mmechano_csr_code": mat.mmechano_csr_code,
                    "mmechano_name": mat.mmechano_name,
                }
                for mat in all_data
            ],
        }
        return result
    elif  category == "techno":
        query = db.query(Techno)
        
        if name_value:
            query = query.filter(Techno.techno_name.ilike(f"%{name_value}%"))
            query = query.order_by(
                case((Techno.techno_name.ilike(f"{name_value}%"), 1), else_=2),
                Techno.techno_name,
            )
        else:
            query = query.order_by(Techno.techno_name)
        
        all_data = query.offset(offset).limit(limit).all()
        count = query.count()
        
        print(f"Query Params - name_value: {name_value}, category: {category}, page: {page}, limit: {limit}")
        print(f"Retrieved Data: {all_data}")
        
        if count == 0:
            return {"count": 0, "techno": []}
        
        result = {
            "count": count,
            "materials": [
                {
                    "techno_csr_code": mat.techno_csr_code,
                    "techno_name": mat.techno_name,
                }
                for mat in all_data
            ],
        }
        return result
    else:
        result = {
            "message": "Category kiritish kerak !!!",
        }
        return result  

